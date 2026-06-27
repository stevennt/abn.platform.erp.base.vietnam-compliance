from abc import ABC, abstractmethod


class SigningProvider(ABC):
    @abstractmethod
    def sign_xml(self, xml_string: str) -> str:
        pass


class MockSigningProvider(SigningProvider):
    def sign_xml(self, xml_string: str) -> str:
        placeholder = "<DSCK>MOCK_SIGNATURE</DSCK>"
        if "</HoaDon>" in xml_string:
            return xml_string.replace("</HoaDon>", f"{placeholder}\n</HoaDon>")
        return xml_string


def get_signing_provider(config=None):
    return MockSigningProvider()
