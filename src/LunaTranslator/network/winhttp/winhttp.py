from ctypes import windll, POINTER, pointer, Structure, sizeof
from ctypes.wintypes import LPCWSTR, DWORD, LPVOID, WORD, BOOL, LPCVOID, LPWSTR, USHORT
from requests import RequestException, Timeout
import windows


# typedef
HINTERNET = LPVOID
INTERNET_PORT = WORD
DWORD_PTR = POINTER(DWORD)
LPDWORD = POINTER(DWORD)
# const
NULL = None
WINHTTP_ACCESS_TYPE_DEFAULT_PROXY = 0
WINHTTP_NO_PROXY_NAME = None
WINHTTP_NO_PROXY_BYPASS = None
INTERNET_DEFAULT_PORT = 0
INTERNET_DEFAULT_HTTP_PORT = 80
INTERNET_DEFAULT_HTTPS_PORT = 443
WINHTTP_NO_REFERER = None
WINHTTP_DEFAULT_ACCEPT_TYPES = None
# WINHTTP_FLAG_REFRESH
WINHTTP_FLAG_SECURE = 0x00800000  # https
WINHTTP_NO_ADDITIONAL_HEADERS = None
WINHTTP_NO_REQUEST_DATA = None
WINHTTP_QUERY_SET_COOKIE = 43
WINHTTP_QUERY_RAW_HEADERS_CRLF = 22
WINHTTP_HEADER_NAME_BY_INDEX = None
WINHTTP_NO_HEADER_INDEX = None
ERROR_INSUFFICIENT_BUFFER = 122
WINHTTP_OPTION_PROXY = 38
WINHTTP_ACCESS_TYPE_NAMED_PROXY = 3
WINHTTP_QUERY_STATUS_CODE = 19
WINHTTP_QUERY_FLAG_NUMBER = 0x20000000
WINHTTP_OPTION_SECURITY_FLAGS = 31
SECURITY_FLAG_IGNORE_UNKNOWN_CA = 0x00000100
SECURITY_FLAG_IGNORE_CERT_WRONG_USAGE = 0x00000200
SECURITY_FLAG_IGNORE_CERT_CN_INVALID = 0x00001000  # bad common name in X509 Cert.
SECURITY_FLAG_IGNORE_CERT_DATE_INVALID = 0x00002000  # expired X509 Cert.
SECURITY_FLAG_IGNORE_ALL_CERT_ERRORS = (
    SECURITY_FLAG_IGNORE_UNKNOWN_CA
    | SECURITY_FLAG_IGNORE_CERT_WRONG_USAGE
    | SECURITY_FLAG_IGNORE_CERT_CN_INVALID
    | SECURITY_FLAG_IGNORE_CERT_DATE_INVALID
)
# function
kernel32 = windll.kernel32
Winhttp = windll.Winhttp
WinHttpOpen = Winhttp.WinHttpOpen
WinHttpOpen.argtypes = LPCWSTR, DWORD, LPCWSTR, LPCWSTR, DWORD
WinHttpOpen.restype = HINTERNET
WinHttpCloseHandle = Winhttp.WinHttpCloseHandle
WinHttpCloseHandle.argtypes = (HINTERNET,)

WinHttpSetTimeouts = Winhttp.WinHttpSetTimeouts
WinHttpSetTimeouts.argtypes = HINTERNET, DWORD, DWORD, DWORD, DWORD
WinHttpSetTimeouts.restype = BOOL

WinHttpConnect = Winhttp.WinHttpConnect
WinHttpConnect.argtypes = HINTERNET, LPCWSTR, INTERNET_PORT, DWORD
WinHttpConnect.restype = HINTERNET
WinHttpOpenRequest = Winhttp.WinHttpOpenRequest
WinHttpOpenRequest.argtypes = (
    HINTERNET,
    LPCWSTR,
    LPCWSTR,
    LPCWSTR,
    LPCWSTR,
    POINTER(LPCWSTR),
    DWORD,
)
WinHttpOpenRequest.restype = HINTERNET
WinHttpSendRequest = Winhttp.WinHttpSendRequest
WinHttpSendRequest.argtypes = HINTERNET, LPCWSTR, DWORD, LPVOID, DWORD, DWORD, DWORD_PTR
WinHttpSendRequest.restype = BOOL
WinHttpReceiveResponse = Winhttp.WinHttpReceiveResponse
WinHttpReceiveResponse.argtypes = HINTERNET, LPVOID
WinHttpReceiveResponse.restype = BOOL
WinHttpQueryDataAvailable = Winhttp.WinHttpQueryDataAvailable
WinHttpQueryDataAvailable.argtypes = HINTERNET, LPDWORD
WinHttpQueryDataAvailable.restype = BOOL
WinHttpReadData = Winhttp.WinHttpReadData
WinHttpReadData.argtypes = HINTERNET, LPVOID, DWORD, LPDWORD
WinHttpReadData.restype = BOOL
WinHttpWriteData = Winhttp.WinHttpWriteData
WinHttpWriteData.argtypes = HINTERNET, LPCVOID, DWORD, LPDWORD
WinHttpWriteData.restype = BOOL
WinHttpQueryHeaders = Winhttp.WinHttpQueryHeaders
WinHttpQueryHeaders.argtypes = HINTERNET, DWORD, LPCWSTR, LPVOID, LPDWORD, LPDWORD
WinHttpQueryHeaders.restype = BOOL
WinHttpSetOption = Winhttp.WinHttpSetOption
WinHttpSetOption.argtypes = HINTERNET, DWORD, LPVOID, DWORD
WinHttpSetOption.restype = BOOL


class WINHTTP_PROXY_INFO(Structure):
    _fields_ = [
        ("dwAccessType", DWORD),
        ("lpszProxy", LPWSTR),
        ("lpszProxyBypass", LPWSTR),
    ]


class AutoWinHttpHandle(HINTERNET):
    def __del__(self):
        if self:
            WinHttpCloseHandle(self)


try:
    WinHttpWebSocketCompleteUpgrade = Winhttp.WinHttpWebSocketCompleteUpgrade
    WinHttpWebSocketCompleteUpgrade.argtypes = HINTERNET, DWORD_PTR
    WinHttpWebSocketCompleteUpgrade.restype = HINTERNET
    WinHttpWebSocketSend = Winhttp.WinHttpWebSocketSend
    WinHttpWebSocketSend.argtypes = HINTERNET, DWORD, LPVOID, DWORD
    WinHttpWebSocketSend.restype = DWORD
    WinHttpWebSocketReceive = Winhttp.WinHttpWebSocketReceive
    WinHttpWebSocketReceive.argtypes = HINTERNET, LPVOID, DWORD, DWORD_PTR, DWORD_PTR
    WinHttpWebSocketReceive.restype = DWORD
    WinHttpWebSocketClose = Winhttp.WinHttpWebSocketClose
    WinHttpWebSocketClose.argtypes = HINTERNET, USHORT, LPVOID, DWORD_PTR
    WinHttpWebSocketClose.restype = DWORD
except:

    def _undefined(*args):
        raise Exception("undefined websocket functions for windows 7-")

    WinHttpWebSocketCompleteUpgrade = WinHttpWebSocketSend = WinHttpWebSocketReceive = (
        WinHttpWebSocketClose
    ) = _undefined

WINHTTP_OPTION_UPGRADE_TO_WEB_SOCKET = 114

WINHTTP_WEB_SOCKET_BINARY_MESSAGE_BUFFER_TYPE = 0
WINHTTP_WEB_SOCKET_BINARY_FRAGMENT_BUFFER_TYPE = 1
WINHTTP_WEB_SOCKET_UTF8_MESSAGE_BUFFER_TYPE = 2
WINHTTP_WEB_SOCKET_UTF8_FRAGMENT_BUFFER_TYPE = 3
WINHTTP_WEB_SOCKET_CLOSE_BUFFER_TYPE = 4
ERROR_SUCCESS = 0
WINHTTP_WEB_SOCKET_SUCCESS_CLOSE_STATUS = 1000


WINHTTP_OPTION_REDIRECT_POLICY = 88
WINHTTP_OPTION_REDIRECT_POLICY_ALWAYS = 2
WINHTTP_OPTION_REDIRECT_POLICY_NEVER = 0


class WinhttpException(RequestException):
    ERROR_INVALID_PARAMETER = 87
    ERROR_INVALID_OPERATION = 4317
    WINHTTP_ERROR_BASE = 12000
    ERROR_WINHTTP_OUT_OF_HANDLES = WINHTTP_ERROR_BASE + 1
    ERROR_WINHTTP_TIMEOUT = WINHTTP_ERROR_BASE + 2
    ERROR_WINHTTP_INTERNAL_ERROR = WINHTTP_ERROR_BASE + 4
    ERROR_WINHTTP_INVALID_URL = WINHTTP_ERROR_BASE + 5
    ERROR_WINHTTP_UNRECOGNIZED_SCHEME = WINHTTP_ERROR_BASE + 6
    ERROR_WINHTTP_NAME_NOT_RESOLVED = WINHTTP_ERROR_BASE + 7
    ERROR_WINHTTP_INVALID_OPTION = WINHTTP_ERROR_BASE + 9
    ERROR_WINHTTP_OPTION_NOT_SETTABLE = WINHTTP_ERROR_BASE + 11
    ERROR_WINHTTP_SHUTDOWN = WINHTTP_ERROR_BASE + 12
    ERROR_WINHTTP_LOGIN_FAILURE = WINHTTP_ERROR_BASE + 15
    ERROR_WINHTTP_OPERATION_CANCELLED = WINHTTP_ERROR_BASE + 17
    ERROR_WINHTTP_INCORRECT_HANDLE_TYPE = WINHTTP_ERROR_BASE + 18
    ERROR_WINHTTP_INCORRECT_HANDLE_STATE = WINHTTP_ERROR_BASE + 19
    ERROR_WINHTTP_CANNOT_CONNECT = WINHTTP_ERROR_BASE + 29
    ERROR_WINHTTP_CONNECTION_ERROR = WINHTTP_ERROR_BASE + 30
    ERROR_WINHTTP_RESEND_REQUEST = WINHTTP_ERROR_BASE + 32
    ERROR_WINHTTP_CLIENT_AUTH_CERT_NEEDED = WINHTTP_ERROR_BASE + 44
    ERROR_WINHTTP_CANNOT_CALL_BEFORE_OPEN = WINHTTP_ERROR_BASE + 100
    ERROR_WINHTTP_CANNOT_CALL_BEFORE_SEND = WINHTTP_ERROR_BASE + 101
    ERROR_WINHTTP_CANNOT_CALL_AFTER_SEND = WINHTTP_ERROR_BASE + 102
    ERROR_WINHTTP_CANNOT_CALL_AFTER_OPEN = WINHTTP_ERROR_BASE + 103
    ERROR_WINHTTP_HEADER_NOT_FOUND = WINHTTP_ERROR_BASE + 150
    ERROR_WINHTTP_INVALID_SERVER_RESPONSE = WINHTTP_ERROR_BASE + 152
    ERROR_WINHTTP_INVALID_HEADER = WINHTTP_ERROR_BASE + 153
    ERROR_WINHTTP_INVALID_QUERY_REQUEST = WINHTTP_ERROR_BASE + 154
    ERROR_WINHTTP_HEADER_ALREADY_EXISTS = WINHTTP_ERROR_BASE + 155
    ERROR_WINHTTP_REDIRECT_FAILED = WINHTTP_ERROR_BASE + 156
    ERROR_WINHTTP_AUTO_PROXY_SERVICE_ERROR = WINHTTP_ERROR_BASE + 178
    ERROR_WINHTTP_BAD_AUTO_PROXY_SCRIPT = WINHTTP_ERROR_BASE + 166
    ERROR_WINHTTP_UNABLE_TO_DOWNLOAD_SCRIPT = WINHTTP_ERROR_BASE + 167
    ERROR_WINHTTP_UNHANDLED_SCRIPT_TYPE = WINHTTP_ERROR_BASE + 176
    ERROR_WINHTTP_SCRIPT_EXECUTION_ERROR = WINHTTP_ERROR_BASE + 177
    ERROR_WINHTTP_NOT_INITIALIZED = WINHTTP_ERROR_BASE + 172
    ERROR_WINHTTP_SECURE_FAILURE = WINHTTP_ERROR_BASE + 175
    ERROR_WINHTTP_SECURE_CERT_DATE_INVALID = WINHTTP_ERROR_BASE + 37
    ERROR_WINHTTP_SECURE_CERT_CN_INVALID = WINHTTP_ERROR_BASE + 38
    ERROR_WINHTTP_SECURE_INVALID_CA = WINHTTP_ERROR_BASE + 45
    ERROR_WINHTTP_SECURE_CERT_REV_FAILED = WINHTTP_ERROR_BASE + 57
    ERROR_WINHTTP_SECURE_CHANNEL_ERROR = WINHTTP_ERROR_BASE + 157
    ERROR_WINHTTP_SECURE_INVALID_CERT = WINHTTP_ERROR_BASE + 169
    ERROR_WINHTTP_SECURE_CERT_REVOKED = WINHTTP_ERROR_BASE + 170
    ERROR_WINHTTP_SECURE_CERT_WRONG_USAGE = WINHTTP_ERROR_BASE + 179
    ERROR_WINHTTP_AUTODETECTION_FAILED = WINHTTP_ERROR_BASE + 180
    ERROR_WINHTTP_HEADER_COUNT_EXCEEDED = WINHTTP_ERROR_BASE + 181
    ERROR_WINHTTP_HEADER_SIZE_OVERFLOW = WINHTTP_ERROR_BASE + 182
    ERROR_WINHTTP_CHUNKED_ENCODING_HEADER_SIZE_OVERFLOW = WINHTTP_ERROR_BASE + 183
    ERROR_WINHTTP_RESPONSE_DRAIN_OVERFLOW = WINHTTP_ERROR_BASE + 184
    ERROR_WINHTTP_CLIENT_CERT_NO_PRIVATE_KEY = WINHTTP_ERROR_BASE + 185
    ERROR_WINHTTP_CLIENT_CERT_NO_ACCESS_PRIVATE_KEY = WINHTTP_ERROR_BASE + 186
    ERROR_WINHTTP_CLIENT_AUTH_CERT_NEEDED_PROXY = WINHTTP_ERROR_BASE + 187
    ERROR_WINHTTP_SECURE_FAILURE_PROXY = WINHTTP_ERROR_BASE + 188
    ERROR_WINHTTP_RESERVED_189 = WINHTTP_ERROR_BASE + 189
    ERROR_WINHTTP_HTTP_PROTOCOL_MISMATCH = WINHTTP_ERROR_BASE + 190
    ERROR_WINHTTP_GLOBAL_CALLBACK_FAILED = WINHTTP_ERROR_BASE + 191
    ERROR_WINHTTP_FEATURE_DISABLED = WINHTTP_ERROR_BASE + 192

    def __init__(self, code) -> None:
        module = None
        if (
            WinhttpException.WINHTTP_ERROR_BASE <= code
            and code <= WinhttpException.ERROR_WINHTTP_FEATURE_DISABLED
        ):
            module = Winhttp._handle
        message = windows.FormatMessage(code, module)
        error = "UNKNOWN ERROR {}".format(code)
        for _ in dir(self):
            if _.startswith("ERROR") and code == getattr(self, _):
                error = _
                break
        if message:
            error += ": {}".format(message)

        super().__init__(error)


def MaybeRaiseException(error):
    if error == ERROR_SUCCESS:
        return
    exception = WinhttpException(error)
    if error == WinhttpException.ERROR_WINHTTP_TIMEOUT:
        raise Timeout(exception)
    raise exception


def MaybeRaiseException0(succ):
    if succ == 0:
        MaybeRaiseException(windows.GetLastError())


def winhttpsetproxy(hreq, proxy):
    proxyInfo = WINHTTP_PROXY_INFO()
    proxyInfo.dwAccessType = WINHTTP_ACCESS_TYPE_NAMED_PROXY
    proxyInfo.lpszProxy = proxy
    proxyInfo.lpszProxyBypass = None
    MaybeRaiseException0(
        WinHttpSetOption(
            hreq, WINHTTP_OPTION_PROXY, pointer(proxyInfo), sizeof(proxyInfo)
        )
    )
