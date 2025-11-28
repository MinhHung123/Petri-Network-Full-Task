import numpy as np
import xml.etree.ElementTree as ET
from typing import List, Optional

class PetriNet:
    def __init__(
        self,
        place_ids: List[str],
        trans_ids: List[str],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,   
        O: np.ndarray, 
        M0: np.ndarray
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0

    @classmethod
    def from_pnml(cls, filename: str) -> "PetriNet":
        """Read a PNML file (PT-net) and build a PetriNet."""
        tree = ET.parse(filename)
        root = tree.getroot()
        import re
        m = re.match(r"\{(.+)\}", root.tag)
        ns_uri = m.group(1) if m else ""
        ns = {"pnml": ns_uri} if ns_uri else {}
        def q(tag: str) -> str:
            return f"pnml:{tag}" if ns_uri else tag
        net = root.find(q("net"), ns)
        if net is None:
            net = root.find(".//" + q("net"), ns)
        if net is None:
            raise ValueError("No <net> element found in PNML file")
        places = net.findall(".//" + q("place"), ns)
        transitions = net.findall(".//" + q("transition"), ns)
        place_ids = [p.attrib.get("id") for p in places]
        trans_ids = [t.attrib.get("id") for t in transitions]
        def get_label(elem: ET.Element, child_tag: str) -> Optional[str]:
            child = elem.find(q(child_tag), ns)
            if child is None:
                return None
            text_elem = child.find(q("text"), ns)
            if text_elem is None or text_elem.text is None:
                return None
            return text_elem.text.strip()
        place_names = [get_label(p, "name") for p in places]
        trans_names = [get_label(t, "name") for t in transitions]
        M0 = np.zeros(len(place_ids), dtype=int)
        for i, p in enumerate(places):
            val = get_label(p, "initialMarking")
            if val:
                try:
                    M0[i] = int(val)
                except ValueError:
                    try:
                        M0[i] = int(float(val))
                    except ValueError:
                        M0[i] = 0
        I = np.zeros((len(trans_ids), len(place_ids)), dtype=int)
        O = np.zeros((len(trans_ids), len(place_ids)), dtype=int)
        place_idx = {pid: i for i, pid in enumerate(place_ids)}
        trans_idx = {tid: i for i, tid in enumerate(trans_ids)}
        arcs = net.findall(".//" + q("arc"), ns)
        def arc_weight(a: ET.Element) -> int:
            ins = a.find(q("inscription"), ns)
            if ins is None:
                return 1
            text_elem = ins.find(q("text"), ns)
            if text_elem is None or text_elem.text is None:
                return 1
            txt = text_elem.text.strip()
            try:
                return int(txt)
            except ValueError:
                try:
                    return int(float(txt))
                except ValueError:
                    return 1
        for a in arcs:
            src = a.attrib.get("source")
            tgt = a.attrib.get("target")
            w = arc_weight(a)

            if src in place_idx and tgt in trans_idx:
                # place -> transition
                I[trans_idx[tgt], place_idx[src]] += w
            elif src in trans_idx and tgt in place_idx:
                # transition -> place
                O[trans_idx[src], place_idx[tgt]] += w

        return cls(place_ids, trans_ids, place_names, trans_names, I, O, M0)
        pass

    def __str__(self) -> str:
        s = []
        s.append("Places: " + str(self.place_ids))
        s.append("Place names: " + str(self.place_names))
        s.append("\nTransitions: " + str(self.trans_ids))
        s.append("Transition names: " + str(self.trans_names))
        s.append("\nI (input) matrix:")
        s.append(str(self.I))
        s.append("\nO (output) matrix:")
        s.append(str(self.O))
        s.append("\nInitial marking M0:")
        s.append(str(self.M0))
        return "\n".join(s)


