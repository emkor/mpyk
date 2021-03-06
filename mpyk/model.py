from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from typing import Dict, Any, Tuple


@dataclass(frozen=True)
class MpykTransLoc:
    """Represents location of transportation unit at specific time"""

    kind: str
    line: str
    course: int
    timestamp: datetime
    lat: float
    lon: float

    @classmethod
    def parse(cls, api_response: Dict[str, Any], timestamp: datetime) -> MpykTransLoc:
        """Parses MPK API response into object"""
        return MpykTransLoc(kind=api_response['type'], line=api_response['name'], course=int(api_response['k']),
                            timestamp=timestamp, lat=api_response['x'], lon=api_response['y'])

    def as_dict(self):
        """For JSON serialization"""
        return {
            "kind": self.kind,
            "line": self.line,
            "course": self.course,
            "lat": self.lat,
            "lon": self.lon,
            "timestamp": self.timestamp.isoformat(timespec='seconds')
        }

    def as_api_dict(self):
        """For MPK API-compatible JSON serialization"""
        return {
            "type": self.kind,
            "name": self.line,
            "k": self.course,
            "x": self.lat,
            "y": self.lon
        }

    def as_values(self) -> Tuple[str, str, str, int, float, float]:
        """For CSV serialization"""
        return (self.timestamp.isoformat(timespec='seconds'),
                self.kind, self.line, self.course, self.lat, self.lon)
