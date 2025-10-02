# tests/pages/base_page.py
from __future__ import annotations
import os
import re
import time
from typing import Optional, Union
from abc import ABC
from playwright.sync_api import Page, Locator, expect

Selector = Union[str, Locator]

class BasePage(ABC):
    """Shared UI helpers for Playwright sync API."""

    def __init__(self, page: Page, *, timeout_ms: int = 30_000) -> None:
        self.page = page
        self.timeout = timeout_ms  # default per-action timeout

    # ---------- internal utilities ----------
    def _loc(self, target: Selector) -> Locator:
        return target if isinstance(target, Locator) else self.page.locator(target)

    def _safe_name(self, raw: str) -> str:
        return re.sub(r"[^A-Za-z0-9._-]+", "_", raw)[:120]

    def _shot(self, prefix: str, target: Optional[Selector] = None) -> str:
        os.makedirs("screenshots", exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        name = self._safe_name(getattr(target, "_selector", str(target))) if target is not None else "page"
        path = f"screenshots/{prefix}_{name}_{stamp}.png"
        self.page.screenshot(path=path, full_page=True)
        return path

    # ---------- navigation ----------
    def navigate_to_url(self, url: str) -> None:
        """Navigate and wait for network to settle."""
        try:
            self.page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        except Exception as e:
            path = self._shot("goto_error")
            raise RuntimeError(f"Failed to navigate to {url}. Screenshot: {path}") from e

    def wait_for_page_load(self) -> None:
        """Wait for load completion/idle network."""
        self.page.wait_for_load_state("load", timeout=self.timeout)
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)

    # ---------- element actions ----------
    def wait_for_element(self, locator: Selector, *, state: str = "visible", timeout: Optional[int] = None) -> None:
        """Wait using Locator.wait_for (preferred over page.wait_for_selector)."""
        try:
            self._loc(locator).wait_for(state=state, timeout=timeout or self.timeout)
        except Exception as e:
            path = self._shot("wait_error", locator)
            raise RuntimeError(f"Wait for element '{locator}' state={state} failed. Screenshot: {path}") from e

    def click_element(self, locator: Selector, *, trial: bool = False, timeout: Optional[int] = None) -> None:
        """Click element with auto-wait for visibility & enabled state."""
        loc = self._loc(locator)
        try:
            expect(loc).to_be_visible(timeout=timeout or self.timeout)
            expect(loc).to_be_enabled(timeout=timeout or self.timeout)
            loc.click(timeout=timeout or self.timeout, trial=trial)
        except Exception as e:
            path = self._shot("click_error", locator)
            raise RuntimeError(f"Click failed on '{locator}'. Screenshot: {path}") from e

    def double_click_element(self, locator: Selector) -> None:
        loc = self._loc(locator)
        try:
            expect(loc).to_be_visible(timeout=self.timeout)
            loc.dblclick(timeout=self.timeout)
        except Exception as e:
            path = self._shot("dblclick_error", locator)
            raise RuntimeError(f"Double-click failed on '{locator}'. Screenshot: {path}") from e

    def right_click_element(self, locator: Selector) -> None:
        loc = self._loc(locator)
        try:
            expect(loc).to_be_visible(timeout=self.timeout)
            loc.click(button="right", timeout=self.timeout)
        except Exception as e:
            path = self._shot("rightclick_error", locator)
            raise RuntimeError(f"Right-click failed on '{locator}'. Screenshot: {path}") from e

    def hover_element(self, locator: Selector) -> None:
        loc = self._loc(locator)
        try:
            expect(loc).to_be_visible(timeout=self.timeout)
            loc.hover(timeout=self.timeout)
        except Exception as e:
            path = self._shot("hover_error", locator)
            raise RuntimeError(f"Hover failed on '{locator}'. Screenshot: {path}") from e

    def scroll_to_element(self, locator: Selector) -> None:
        self._loc(locator).scroll_into_view_if_needed(timeout=self.timeout)

    # ---------- text / input ----------
    def fill_text(
        self,
        locator: Selector,
        text: str,
        *,
        verify: bool = True,
        sensitive: bool = False,
        timeout: Optional[int] = None,
    ) -> None:
        """Clear+set value via Locator.fill()."""
        loc = self._loc(locator)
        to = timeout or self.timeout
        try:
            expect(loc).to_be_visible(timeout=to)
            expect(loc).to_be_enabled(timeout=to)
            loc.fill(text, timeout=to)
            if verify and not sensitive:
                expect(loc).to_have_value(text, timeout=to)
        except Exception as e:
            path = self._shot("fill_error", locator)
            raise RuntimeError(f"Fill failed on '{locator}'. Screenshot: {path}") from e

    def type_text(
        self,
        locator: Selector,
        text: str,
        *,
        clear_first: bool = True,
        press_tab: bool = False,
        timeout: Optional[int] = None,
    ) -> None:
        """Keystroke-by-keystroke entry for inputs that require input events."""
        loc = self._loc(locator)
        to = timeout or self.timeout
        try:
            expect(loc).to_be_visible(timeout=to)
            expect(loc).to_be_enabled(timeout=to)
            loc.click(timeout=to)
            if clear_first:
                loc.press("ControlOrMeta+A", timeout=to)
                loc.press("Delete", timeout=to)
            loc.type(text, timeout=to)
            if press_tab:
                loc.press("Tab", timeout=to)
        except Exception as e:
            path = self._shot("type_error", locator)
            raise RuntimeError(f"Type failed on '{locator}'. Screenshot: {path}") from e

    # ---------- select, upload ----------
    def select_option(self, locator: Selector, value: str | dict | list[str] | list[dict]) -> None:
        """Supports single or multiple value dicts ({'label': 'x'}, {'value': 'y'})."""
        loc = self._loc(locator)
        try:
            expect(loc).to_be_visible(timeout=self.timeout)
            loc.select_option(value, timeout=self.timeout)
        except Exception as e:
            path = self._shot("select_error", locator)
            raise RuntimeError(f"Select option failed on '{locator}'. Screenshot: {path}") from e

    def upload_file(self, locator: Selector, file_path: str | list[str]) -> None:
        loc = self._loc(locator)
        try:
            expect(loc).to_be_visible(timeout=self.timeout)
            loc.set_input_files(file_path, timeout=self.timeout)
        except Exception as e:
            path = self._shot("upload_error", locator)
            raise RuntimeError(f"Upload failed on '{locator}'. Screenshot: {path}") from e

    # ---------- getters / assertions ----------
    def get_text(self, locator: Selector, *, strict: bool = False) -> str:
        """Return visible inner text (waits attached); fallback to empty string on failure."""
        loc = self._loc(locator)
        try:
            expect(loc).to_be_attached(timeout=self.timeout)
            return (loc.inner_text(timeout=self.timeout) if strict else (loc.text_content(timeout=self.timeout) or "")).strip()
        except Exception:
            return ""

    def is_element_visible(self, locator: Selector) -> bool:
        try:
            return self._loc(locator).is_visible()
        except Exception:
            return False

    def get_attribute(self, locator: Selector, attribute: str) -> str:
        try:
            val = self._loc(locator).get_attribute(attribute, timeout=self.timeout)
            return val or ""
        except Exception:
            return ""

    def verify_element_contains_text(self, locator: Selector, expected_text: str) -> None:
        expect(self._loc(locator)).to_contain_text(expected_text, timeout=self.timeout)

    def verify_element_has_text(self, locator: Selector, expected_text: str) -> None:
        expect(self._loc(locator)).to_have_text(expected_text, timeout=self.timeout)

    # ---------- keyboard ----------
    def press_key(self, key: str) -> None:
        self.page.keyboard.press(key)

    def type_using_keyboard(self, text: str, *, delay_ms: int = 0) -> None:
        self.page.keyboard.type(text, delay=delay_ms)

    # ---------- page info ----------
    def get_current_url(self) -> str:
        return self.page.url

    def get_page_title(self) -> str:
        return self.page.title()
