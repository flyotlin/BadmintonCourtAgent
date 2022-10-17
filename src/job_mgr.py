from src.job import AyeJob


class JobMgr:
    def __init__(self) -> None:
        pass

    def has(self, job: AyeJob) -> bool:
        if job._is_in_jobqueue():
            return True
        return False

    def create(self, job: AyeJob) -> bool:
        if not job._is_in_database():
            job._create_in_database()
        if not job._is_in_jobqueue():
            job._create_in_jobqueue()
