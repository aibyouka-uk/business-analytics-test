import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import successors as s

DB = s.load()


def ids(name):
    return s.find_entities(DB, name)


def test_name_variants_match_inttel():
    for n in ["Интел-Тел", "Инт-Тел", "int-tel", "Intel-Tel", "ООО Инт-Тел"]:
        assert ids(n) == ["inttel"], n


def test_other_names():
    assert "gorcom" in ids("gorcom") and "gorcom" in ids("Горком")
    assert ids("Город Телеком") == ["gorod_telecom"]
    assert "sevensky_brand" in ids("sevensky")


def test_inttel_leads_to_sevensky_ooo():
    chain = s.successors(DB, ["inttel"])
    assert "sevensky_ooo" in {e["to"] for e, _ in chain}


def test_gorcom_chain_reaches_sevensky_in_period():
    lo, hi = s.parse_period("2014-2016")
    assert "sevensky_brand" in {e["to"] for e, _ in s.successors(DB, ["gorcom"], lo, hi)}


def test_period_filters_out_later_edges():
    lo, hi = s.parse_period("2010")
    assert "sevensky_brand" not in {e["to"] for e, _ in s.successors(DB, ["gorcom"], lo, hi)}


def test_min_confidence_filters_unverified():
    assert s.successors(DB, ["gorod_telecom"], min_conf="low") == []


def test_report_output():
    text, code = s.report(DB, "Интел-Тел", "2018-2020")
    assert code == 0 and "Севен Скай" in text and "Current service point" in text
    assert s.report(DB, "Нет такого")[1] == 1
