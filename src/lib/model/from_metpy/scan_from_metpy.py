import math

import numpy as np
from metpy.io import Level2File

from lib.model.record import Record
from lib.model.scan import Scan

rayLength = 2000

REF = b"REF"
VEL = b"VEL"


def scanFromLevel2Data(record: Record, data: Level2File):
    reflectivitySweeps = []
    velocitySweeps = []

    for elevationHeader, sweep in zip(data.vcp_info.els, data.sweeps):
        elevation = elevationHeader.el_angle

        # Some elevations have a constant phase, where reflectivity and velocity are
        # recorded together. Others have a split phase, where reflectivity and velocity
        # are recorded on separate passes.
        isConstantPhase = elevationHeader.channel_config == "Constant Phase"
        isSplitPhase = elevationHeader.channel_config == "SZ2 Phase"

        # The third option is random phase, disregard
        if not (isConstantPhase or isSplitPhase):
            continue

        waveform = elevationHeader.waveform
        isReflectivitySweep = isConstantPhase or waveform == "Contiguous Surveillance"
        isVelocitySweep = isConstantPhase or "Doppler" in waveform

        if isReflectivitySweep:
            # Skip any elevations for which we have already accepted a sweep
            if np.any(np.isclose(elevation, [data[0] for data in reflectivitySweeps])):
                continue

            reflectivitySweeps.append((elevation, sweep))

        if isVelocitySweep:
            if np.any(np.isclose(elevation, [data[0] for data in velocitySweeps])):
                continue

            velocitySweeps.append((elevation, sweep))

    # Sort sweeps by elevation angle
    reflectivitySweeps = sorted(reflectivitySweeps)
    velocitySweeps = sorted(velocitySweeps)

    reflectivityElevations = [data[0] for data in reflectivitySweeps]
    velocityElevations = [data[0] for data in velocitySweeps]

    if not np.allclose(reflectivityElevations, velocityElevations):
        raise Exception("Reflectivity and velocity data do not match")

    reflectivityLayers = []
    velocityLayers = []

    first = 0
    spacing = 0

    for data in reflectivitySweeps:
        rays = []

        for ray in data[1]:
            rays.append(rayFromLevel2Data(ray, REF))

        sweep = sorted(rays)
        first = sweep[0][1]
        spacing = sweep[0][2]
        sweepReflectivity = np.stack(tuple(ray[3] for ray in sweep))

        # TODO this is a bit of a hack to make all of the sweeps have the same
        # number of rays. This should be cleaned up later
        if len(sweep) < 500:
            sweepReflectivity = np.repeat(sweepReflectivity, repeats=2, axis=0)

        reflectivityLayers.append(sweepReflectivity)

    for data in velocitySweeps:
        rays = []

        for ray in data[1]:
            rays.append(rayFromLevel2Data(ray, VEL))

        sweep = sorted(rays)
        first = sweep[0][1]
        spacing = sweep[0][2]
        sweepVelocity = np.stack(tuple(ray[3] for ray in sweep))

        # TODO this is a bit of a hack to make all of the sweeps have the same
        # number of rays. This should be cleaned up later
        if len(sweep) < 500:
            sweepVelocity = np.repeat(sweepVelocity, repeats=2, axis=0)

        velocityLayers.append(sweepVelocity)

    # TODO this is a bit of a hack to get an empty sweep on the top and bottom.
    # This is necessary to generate closed geometry on the top and bottom.
    emptyRef = np.empty(reflectivityLayers[0].shape)
    emptyRef[:] = np.nan

    reflectivityLayers.insert(0, emptyRef)
    reflectivityLayers.append(emptyRef)

    velocityLayers.insert(0, emptyRef)
    velocityLayers.append(emptyRef)

    elevations = reflectivityElevations
    elevations.insert(0, 0)
    elevations.append(elevations[-1] + elevations[-1] - elevations[-2])
    elevations = np.array(elevations)

    azimuths = np.linspace(0, 359.5, 720)
    ranges = np.linspace(first, first + rayLength * spacing, rayLength + 1)

    reflectivity = np.stack(reflectivityLayers)
    velocity = np.stack(velocityLayers)

    return Scan(record, elevations, azimuths, ranges, reflectivity, velocity)


def rayFromLevel2Data(level2Ray, dataType):
    header = level2Ray[0]
    azimuth = math.radians(header.az_angle)

    reflectivity_header = level2Ray[4][dataType][0]
    first = reflectivity_header.first_gate
    spacing = reflectivity_header.gate_width

    reflectivity = level2Ray[4][dataType][1]

    # TODO this is a bit of a hack to make all of the rays the same length.
    # This should be cleaned up later
    reflectivity = np.pad(
        reflectivity,
        (1, rayLength - reflectivity.shape[0]),
        mode="constant",
        constant_values=(np.nan),
    )

    # Account for the nan added to the start of the reflectivity list
    first = first - spacing

    return azimuth, first, spacing, reflectivity
