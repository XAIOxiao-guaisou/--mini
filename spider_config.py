"""爬虫运行配置（轻量版）。

这个文件主要用于 QUICKSTART_ENHANCED.py 的环境自检与“查看当前配置”功能。
当前项目的核心配置以 config.py 为准；此处仅做聚合展示。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import config


@dataclass(frozen=True)
class CurrentConfig:
    edge_path: str
    user_data_path: str

    require_china_network: bool
    china_network_strict: bool
    china_proxy_server: str

    enable_wecom_push: bool
    top_n_results: int


def get_current_config() -> dict:
    """返回当前生效配置（用于诊断展示）。"""
    cfg = CurrentConfig(
        edge_path=getattr(config, "EDGE_PATH", ""),
        user_data_path=getattr(config, "USER_DATA_PATH", ""),
        require_china_network=bool(getattr(config, "REQUIRE_CHINA_NETWORK", False)),
        china_network_strict=bool(getattr(config, "CHINA_NETWORK_STRICT", True)),
        china_proxy_server=str(getattr(config, "CHINA_PROXY_SERVER", "") or "").strip(),
        enable_wecom_push=bool(getattr(config, "ENABLE_WECOM_PUSH", False)),
        top_n_results=int(getattr(config, "TOP_N_RESULTS", 5)),
    )
    return asdict(cfg)


def main() -> None:
    cfg = get_current_config()
    print("=" * 60)
    print("当前配置（聚合展示）")
    print("=" * 60)
    for k, v in cfg.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
