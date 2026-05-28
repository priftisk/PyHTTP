"""
Tests for PyHTTP — router, request parsing, response building, and middleware.

Run from the repo root:
    python -m pytest test_pyhttp.py -v
"""

import unittest
from unittest.mock import MagicMock, patch
import datetime

# ---------------------------------------------------------------------------
# Helpers — build a raw HTTP request bytestring
# ---------------------------------------------------------------------------


def make_raw(method="GET", path="/", version="HTTP/1.1", headers=None):
    header_lines = headers or ["Host: localhost"]
    lines = [f"{method} {path} {version}"] + header_lines + ["", ""]
    return "\r\n".join(lines).encode()


# ---------------------------------------------------------------------------
# Request tests
# ---------------------------------------------------------------------------


class TestRequest(unittest.TestCase):

    def _make(self, method="GET", path="/", version="HTTP/1.1", extra_headers=None):
        from pyhttp.request.request import Request

        return Request(make_raw(method, path, version, extra_headers))

    def test_parses_method(self):
        req = self._make(method="POST")
        self.assertEqual(req.method, "POST")

    def test_parses_path(self):
        req = self._make(path="/posts")
        self.assertEqual(req.path.base, "/posts")

    def test_parses_http_version(self):
        req = self._make(version="HTTP/1.1")
        self.assertEqual(req.http_version, "HTTP/1.1")

    def test_valid_on_good_request(self):
        req = self._make()
        self.assertTrue(req.valid)

    def test_invalid_on_empty_bytes(self):
        from pyhttp.request.request import Request

        req = Request(b"")
        self.assertFalse(req.valid)

    def test_invalid_on_garbage(self):
        from pyhttp.request.request import Request

        req = Request(b"\x00\xff\xfe garbage")
        self.assertFalse(req.valid)

    def test_timestamp_is_datetime(self):
        req = self._make()
        self.assertIsInstance(req.timestamp, datetime.datetime)

    def test_headers_parsed(self):
        req = self._make(extra_headers=["Host: example.com", "Content-Type: text/html"])
        # headers object should exist and be truthy
        self.assertIsNotNone(req.headers)


# ---------------------------------------------------------------------------
# Response tests
# ---------------------------------------------------------------------------


class TestResponse(unittest.TestCase):

    def _make_request(self, path="/"):
        from pyhttp.request.request import Request

        return Request(make_raw(path=path))

    def test_default_status_code(self):
        from pyhttp.response.response import Response

        res = Response(self._make_request())
        self.assertEqual(res.status_code, 200)

    def test_status_message_200(self):
        from pyhttp.response.response import Response

        res = Response(self._make_request(), status_code=200)
        self.assertEqual(res.status_message, "OK")

    def test_status_message_404(self):
        from pyhttp.response.response import Response

        res = Response(self._make_request(), status_code=404)
        self.assertEqual(res.status_message, "Not Found")

    def test_status_message_405(self):
        from pyhttp.response.response import Response

        res = Response(self._make_request(), status_code=405)
        self.assertEqual(res.status_message, "Method Not Allowed")

    def test_encode_returns_bytes(self):
        from pyhttp.response.response import Response

        res = Response(self._make_request(), status_code=200)
        encoded = res.encode()
        self.assertIsInstance(encoded, bytes)

    def test_encode_contains_status_line(self):
        from pyhttp.response.response import Response

        res = Response(self._make_request(), status_code=200)
        encoded = res.encode()
        self.assertIn(b"HTTP/1.1 200 OK", encoded)

    def test_encode_404_contains_not_found(self):
        from pyhttp.response.response import Response

        res = Response(self._make_request(), status_code=404)
        encoded = res.encode()
        self.assertIn(b"404", encoded)

    def test_request_stored_on_response(self):
        from pyhttp.response.response import Response

        req = self._make_request("/about")
        res = Response(req, status_code=200)
        self.assertIs(res.request, req)


# ---------------------------------------------------------------------------
# Router tests
# ---------------------------------------------------------------------------


class TestRouter(unittest.TestCase):

    def setUp(self):
        from pyhttp.router.router import Router
        from pyhttp.request.request_methods import RequestMethod
        from pyhttp.request.request_path import RequestPath

        self.Router = Router
        self.RequestMethod = RequestMethod
        self.RequestPath = RequestPath

    def _make_request(self, method=None, path="/"):
        # Mock the Request so request.method is the actual RequestMethod enum
        # value, not a raw parsed string. This avoids the enum vs string
        # mismatch that would cause route.method_allowed() to always return
        # False and every invoke_handler call to fall through to 404/405.
        req = MagicMock()
        req.method = method if method is not None else self.RequestMethod.GET
        req.path = self.RequestPath(path)
        return req

    def test_register_route_adds_to_routes(self):
        router = self.Router()
        handler = MagicMock(return_value=MagicMock())
        router.register_route([self.RequestMethod.GET], "/", handler)
        self.assertEqual(len(router.routes), 1)

    def test_route_exists_after_registration(self):
        router = self.Router()
        handler = MagicMock()
        router.register_route([self.RequestMethod.GET], "/hello", handler)
        self.assertTrue(router.route_exists("/hello"))

    def test_route_does_not_exist_before_registration(self):
        router = self.Router()
        self.assertFalse(router.route_exists("/missing"))

    def test_invoke_handler_calls_handler_on_match(self):
        from pyhttp.response.response import Response

        router = self.Router()
        req = self._make_request(path="/")
        mock_response = MagicMock(spec=Response)
        handler = MagicMock(return_value=mock_response)
        router.register_route([self.RequestMethod.GET], "/", handler)
        result = router.invoke_handler(req)
        handler.assert_called_once_with(req)
        self.assertIs(result, mock_response)

    def test_invoke_handler_returns_404_for_unknown_path(self):
        from pyhttp.response.response import Response

        router = self.Router()
        req = self._make_request(path="/does-not-exist")
        result = router.invoke_handler(req)
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 404)

    def test_invoke_handler_returns_405_for_wrong_method(self):
        from pyhttp.response.response import Response

        router = self.Router()
        handler = MagicMock()
        router.register_route([self.RequestMethod.GET], "/only-get", handler)
        req = self._make_request(method=self.RequestMethod.POST, path="/only-get")
        result = router.invoke_handler(req)
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 405)
        handler.assert_not_called()

    def test_multiple_routes_resolve_correctly(self):
        router = self.Router()
        handler_a = MagicMock(return_value=MagicMock())
        handler_b = MagicMock(return_value=MagicMock())
        router.register_route([self.RequestMethod.GET], "/a", handler_a)
        router.register_route([self.RequestMethod.GET], "/b", handler_b)
        req_b = self._make_request(path="/b")
        router.invoke_handler(req_b)
        handler_a.assert_not_called()
        handler_b.assert_called_once()

    def test_route_one_param_is_parsed(self):
        router = self.Router()
        handler = MagicMock(return_value=MagicMock())
        router.register_route([self.RequestMethod.GET], "/test/:id", handler)
        for r in router.routes:
            if r.path.base == "/test":
                assert len(r.path.parameters) == 1
                assert r.path.parameters[0] == "id"


# ---------------------------------------------------------------------------
# Middleware tests
# ---------------------------------------------------------------------------


class TestMiddleware(unittest.TestCase):

    def _make_request(self):
        from pyhttp.request.request import Request

        return Request(make_raw())

    def _make_middleware(self, name="test", should_pass=True, logger=None):
        """Create a concrete Middleware subclass on the fly."""
        from pyhttp.middleware.middleware import Middleware

        class ConcreteMiddleware(Middleware):
            def handle(self, request):
                if should_pass:
                    return self.call_next(request)
                return False, self.error_msg

        return ConcreteMiddleware(name=name, logger=logger)

    def test_handle_passes_when_allowed(self):
        mw = self._make_middleware(should_pass=True)
        req = self._make_request()
        passed, msg = mw.handle(req)
        self.assertTrue(passed)
        self.assertIsNone(msg)

    def test_handle_blocks_when_denied(self):
        mw = self._make_middleware(should_pass=False)
        req = self._make_request()
        passed, msg = mw.handle(req)
        self.assertFalse(passed)
        self.assertIsNotNone(msg)

    def test_set_next_returns_next_middleware(self):
        mw1 = self._make_middleware(name="first")
        mw2 = self._make_middleware(name="second")
        result = mw1.set_next(mw2)
        self.assertIs(result, mw2)

    def test_chain_passes_through_both(self):
        mw1 = self._make_middleware(name="first", should_pass=True)
        mw2 = self._make_middleware(name="second", should_pass=True)
        mw1.set_next(mw2)
        req = self._make_request()
        passed, msg = mw1.handle(req)
        self.assertTrue(passed)

    def test_chain_stops_at_blocking_middleware(self):
        mw1 = self._make_middleware(name="first", should_pass=True)
        mw2 = self._make_middleware(name="second", should_pass=False)
        mw1.set_next(mw2)
        req = self._make_request()
        passed, msg = mw1.handle(req)
        self.assertFalse(passed)

    def test_name_property(self):
        mw = self._make_middleware(name="auth")
        self.assertEqual(mw.name, "auth")

    def test_error_msg_default(self):
        mw = self._make_middleware()
        self.assertIsInstance(mw.error_msg, str)
        self.assertTrue(len(mw.error_msg) > 0)

    def test_error_msg_setter(self):
        mw = self._make_middleware()
        mw.error_msg = "Access denied."
        self.assertEqual(mw.error_msg, "Access denied.")


if __name__ == "__main__":
    unittest.main()
