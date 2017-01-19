class WorkerNotSpecified(Exception):
    pass


class ResourcesError(Exception):
    pass


class DAGCycleError(Exception):
    pass


class SubTaskFailed(Exception):
    pass
