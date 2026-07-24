from uuid import UUID

from oslo_api.analysis.persistence import evidence_reference

DOCUMENT_ID = UUID("018f9f7e-8de2-7000-8000-000000000099")


def test_evidence_reference_preserves_each_source_locator() -> None:
    assert evidence_reference(
        document_id=DOCUMENT_ID,
        ordinal=0,
        locator={"kind": "pdf_page", "page": 4},
    ).endswith(":page:4:fragment:0")
    assert evidence_reference(
        document_id=DOCUMENT_ID,
        ordinal=1,
        locator={"kind": "docx_section", "section": "Delivery Plan"},
    ).endswith(":section:Delivery%20Plan:fragment:1")
    assert evidence_reference(
        document_id=DOCUMENT_ID,
        ordinal=2,
        locator={"kind": "pptx_slide", "slide": 7},
    ).endswith(":slide:7:fragment:2")
    assert evidence_reference(
        document_id=DOCUMENT_ID,
        ordinal=3,
        locator={"kind": "xlsx_range", "sheet": "Budget FY27", "cell_range": "A1:D20"},
    ).endswith(":sheet:Budget%20FY27:range:A1%3AD20:fragment:3")
