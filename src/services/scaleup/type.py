""" File all contain all rest body definition"""
import re

from pydantic import BaseModel, validator


class AutosclaerPayload(BaseModel):
    """Autoscaler payload body"""
    service_url: str = ""
    interval: int = 15

    @validator('interval', pre=True)
    def validate_interval(cls, v):  # pylint: disable=no-self-argument
        """Validate interval"""
        if v < 0:
            raise ValueError("Interval value must be greater than zero.")
        return v

    @validator('service_url', pre=True)
    def validate_service_url(cls, v):  # pylint: disable=no-self-argument
        """Validate url"""
        url_pattern = (
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$'  # optional path
        )
        if re.match(url_pattern, v, re.IGNORECASE) is None:
            raise ValueError("Invalid URL.")
        return v
