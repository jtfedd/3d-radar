from lib.app.state import AppState
from lib.model.data_query import DataQuery
from lib.model.time_query import TimeQuery


def dataQueryFromState(state: AppState) -> DataQuery:
    radar = state.station.value
    minutes = state.loopMinutes.value
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
        minutes=minutes,
        time=time,
    )


def applyDataQueryToState(state: AppState, query: DataQuery) -> None:
    state.station.setValue(query.radar)
    state.loopMinutes.setValue(query.minutes)
    state.latest.setValue(query.time is None)
    if query.time is not None:
        state.year.setValue(query.time.year)
        state.month.setValue(query.time.month)
        state.day.setValue(query.time.day)
        state.time.setValue(query.time.time)
