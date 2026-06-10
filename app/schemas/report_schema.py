from pydantic import BaseModel


class ReportSummaryResponse(BaseModel):
    total_students: int
    active_students: int
    total_counseling_records: int
    open_counseling_records: int
    in_progress_counseling_records: int
    resolved_counseling_records: int
    total_assessments: int
    counseling_records_by_status: dict[str, int]
    assessments_by_type: dict[str, int]