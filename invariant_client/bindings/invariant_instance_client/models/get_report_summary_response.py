from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict

if TYPE_CHECKING:
    from ..models.report import Report
    from ..models.get_report_summary_response_status import (
        GetReportSummaryResponseStatus,
    )
    from ..models.get_report_summary_response_summary import (
        GetReportSummaryResponseSummary,
    )


T = TypeVar("T", bound="GetReportSummaryResponse")


@_attrs_define
class GetReportSummaryResponse:
    """
    Attributes:
        report (Report):
        summary (GetReportSummaryResponseSummary):
        status (GetReportSummaryResponseStatus):
    """

    report: "Report"
    summary: "GetReportSummaryResponseSummary"
    status: "GetReportSummaryResponseStatus"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        report = self.report.to_dict()

        summary = self.summary.to_dict()

        status = self.status.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "report": report,
                "summary": summary,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.report import Report
        from ..models.get_report_summary_response_status import (
            GetReportSummaryResponseStatus,
        )
        from ..models.get_report_summary_response_summary import (
            GetReportSummaryResponseSummary,
        )

        d = src_dict.copy()
        report = Report.from_dict(d.pop("report"))

        summary = GetReportSummaryResponseSummary.from_dict(d.pop("summary"))

        status = GetReportSummaryResponseStatus.from_dict(d.pop("status"))

        get_report_summary_response = cls(
            report=report,
            summary=summary,
            status=status,
        )

        get_report_summary_response.additional_properties = d
        return get_report_summary_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
