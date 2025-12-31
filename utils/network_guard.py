"""网络环境守卫：确保脚本运行时使用中国网络出口。

说明：
- 代码层面无法“强制把你的网络切到中国”，只能：
  1) 检测当前出口位置是否为中国；若不是则中止并提示你切换网络；
  2) 或在配置了中国代理时，尽量通过代理出站。
- 这里优先使用国内可访问的 IP 查询接口。
"""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class ChinaNetworkReport:
    ok: bool
    reason: str
    ip: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = None


def _http_get_text(url: str, timeout: float = 5.0) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return data.decode("utf-8", errors="ignore")


def _parse_sohu_cityjson(text: str) -> Tuple[Optional[str], Optional[str]]:
    # 形如：var returnCitySN = {"cip": "x.x.x.x", "cname": "北京市"};
    m = re.search(r"returnCitySN\s*=\s*(\{.*?\})\s*;", text, flags=re.S)
    if not m:
        return None, None
    try:
        obj = json.loads(m.group(1))
        return obj.get("cip"), obj.get("cname")
    except Exception:
        return None, None


def _parse_ipip(text: str) -> Tuple[Optional[str], Optional[str]]:
    # 形如：当前 IP：1.2.3.4 来自于：中国 北京 北京
    ip = None
    loc = None
    m = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", text)
    if m:
        ip = m.group(1)
    if "来自于" in text:
        loc = text.strip().replace("\n", " ")
    return ip, loc


def check_china_network(timeout: float = 5.0) -> ChinaNetworkReport:
    """检测当前出口是否为中国网络。

    Returns:
        ChinaNetworkReport(ok=True/False)
    """
    # 国内常用可访问的接口（按稳定性排序）
    sources = [
        ("sohu_cityjson", "https://pv.sohu.com/cityjson?ie=utf-8"),
        ("ipip", "https://myip.ipip.net"),
    ]

    last_err = None
    for name, url in sources:
        try:
            text = _http_get_text(url, timeout=timeout)
            if name == "sohu_cityjson":
                ip, loc = _parse_sohu_cityjson(text)
            else:
                ip, loc = _parse_ipip(text)

            # 判断是否中国
            joined = " ".join([x for x in [loc, text] if x])
            is_cn = ("中国" in joined) or ("China" in joined)

            if is_cn:
                return ChinaNetworkReport(ok=True, reason="china_network_ok", ip=ip, location=loc, source=name)

            # 能解析到位置但不是中国
            if loc or ip:
                return ChinaNetworkReport(ok=False, reason="egress_not_in_china", ip=ip, location=loc, source=name)

        except Exception as e:
            last_err = str(e)
            continue

    return ChinaNetworkReport(ok=False, reason=f"network_check_failed: {last_err or 'unknown'}")


def ensure_china_network(*, strict: bool = True, timeout: float = 5.0) -> ChinaNetworkReport:
    """确保处于中国网络，否则抛出 RuntimeError。"""
    report = check_china_network(timeout=timeout)
    if report.ok:
        return report

    if strict:
        detail = []
        if report.ip:
            detail.append(f"ip={report.ip}")
        if report.location:
            detail.append(f"location={report.location}")
        if report.source:
            detail.append(f"source={report.source}")
        extra = ("; ".join(detail)) if detail else report.reason
        raise RuntimeError(
            "检测到当前网络出口可能不在中国，已按要求停止运行。\n"
            f"详情：{extra}\n"
            "解决方案：\n"
            "1) 切换到中国网络（国内宽带/国内移动网络/中国线路 VPN）。\n"
            "2) 或配置中国代理：设置环境变量 CHINA_PROXY_SERVER=http(s)://host:port，然后重试。"
        )

    return report
