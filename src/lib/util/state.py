from lib.app.state import AppState
from lib.model.data_query import DataQuery
from lib.model.time_query import TimeQuery


def dataQueryFromState(state: AppState) -> DataQuery:
    radar = state.station.value
    frames = state.frames.value
    time: TimeQuery | None = None
    if not state.latest.value:
        time = TimeQuery(
            year=state.year.value,
            month=state.month.value,
            day=state.day.value,
            time=state.time.value,
        )

    return DataQuery(
        radar=radar,
        frames=frames,
        time=time,
    )


def applyDataQueryToState(state: AppState, query: DataQuery) -> None:
    state.station.setValue(query.radar)
    state.frames.setValue(query.frames)
    state.latest.setValue(query.time is None)
    if query.time is not None:
        state.year.setValue(query.time.year)
        state.month.setValue(query.time.month)
        state.day.setValue(query.time.day)
        state.time.setValue(query.time.time)
