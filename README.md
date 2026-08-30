<div align="center">

# 🏠 Duy's Home Assistant Add-ons

**Practical Home Assistant add-ons for AI routing, computer vision, camera integrations, robot vacuums, voice control, and media automation.**

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Add--ons-41BDF5?logo=home-assistant&logoColor=white)](https://www.home-assistant.io/)
[![Repository](https://img.shields.io/badge/Add--on-Repository-blue)](https://github.com/trankhanhduy2929-beep/Duy_Home_Assistant_Addons)
[![GitHub last commit](https://img.shields.io/github/last-commit/trankhanhduy2929-beep/Duy_Home_Assistant_Addons)](https://github.com/trankhanhduy2929-beep/Duy_Home_Assistant_Addons/commits/main)
[![License](https://img.shields.io/badge/Public%20repository-MIT-green)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?logo=github-sponsors)](https://github.com/sponsors/trankhanhduy2929-beep)

**English** · [Tiếng Việt](README_VI.md)

</div>

---

## About this repository

This is the public installation and documentation repository for add-ons maintained by **Trần Khánh Duy**.

It contains Home Assistant add-on manifests, icons, documentation, release information, and links to prebuilt container images. Some add-ons are distributed as prebuilt images while their implementation source code is maintained privately.

> [!IMPORTANT]
> The MIT License in this repository applies only to files committed to this public repository. It does not automatically apply to private source code or separately distributed container images. See [NOTICE.md](NOTICE.md).

## Installation

1. Open **Home Assistant**.
2. Go to **Settings → Add-ons → Add-on Store**.
3. Open the **⋮** menu in the top-right corner.
4. Select **Repositories**.
5. Add this repository:

```text
https://github.com/trankhanhduy2929-beep/my_hass_addon_public
```

6. Return to the Add-on Store and install the add-on you need.

## Featured add-on

### 🤖 AI Proxy Router

A centralized OpenAI-compatible AI gateway for Home Assistant with:

- Multiple AI providers and API keys
- Intelligent text and vision routing
- Automatic failover and provider recovery
- Proxy Key isolation and usage limits
- OpenAI Codex OAuth
- Provider health monitoring and Telegram alerts
- Bolt Token Saver: RTK, Headroom, Caveman, and Ponytail

**Current public manifest version:** `1.9.0`  
**Supported architectures:** `amd64`, `aarch64`

[Read the complete AI Proxy Router documentation](ai_proxy_router/README.md)

## Other add-ons

This repository also includes add-ons for:

- HANET camera, FaceID, access control, LPR, and attendance integration
- Ecovacs cloud, MQTT, maps, sensors, and robot control
- AI camera/image description
- Voice actions and Vietnamese voice workflows
- YouTube and media automation
- Experimental Home Assistant utilities

Open an add-on folder to view its manifest and documentation.

<!-- AUTO-ADDON-CATALOG:START -->
## Add-on catalog

This table is generated automatically from the private release catalog after successful image builds.

| Add-on | Version | Stage | Architectures | Documentation |
|---|---:|---|---|---|
| HANET Connect Gateway | `0.10.5` | experimental | `amd64, aarch64` | [Open](addon_hanet_connect/README.md) |
| AI Proxy Router | `1.14.0` | stable | `amd64, aarch64` | [Open](ai_proxy_router/README.md) |
| Chấm Công ZKTeco | `2.0.5` | stable | `amd64, aarch64` | [Open](cham_cong_zkteco/README.md) |
| Ecovacs China Backend | `1.3.5` | stable | `amd64, aarch64` | [Open](ecovacs_cn_backend/README.md) |
| Ecovacs Private Gateway | `2.1.3` | stable | `amd64, aarch64` | [Open](ecovacs_gateway/README.md) |
| Hanet Camera Bridge | `2.5.2` | stable | `amd64, aarch64` | [Open](hanet_bridge/README.md) |
| Hanet Camera Bridge Pro | `3.0.9` | stable | `amd64, aarch64` | [Open](hanet_bridge_pro/README.md) |
| AI Vision Entity Describer | `1.1.3` | stable | `amd64, aarch64` | [Open](hass-ai-vision-addon/README.md) |
| PicoClaw | `0.4.4` | stable | `amd64, aarch64` | [Open](picoclaw/README.md) |
| HA Camera Face ID | `2.2.0` | stable | `amd64, aarch64` | [Open](rtsp_face_bridge/README.md) |
| Voice Action Bridge VI Lite | `1.0.4` | stable | `amd64, aarch64` | [Open](voice-action-bridge-vi-lite/README.md) |
| YouTube Music Lite | `2.4.0` | stable | `amd64, aarch64` | [Open](youtube_cast_addon/README.md) |
| YouTube Pro | `5.3.1` | stable | `amd64, aarch64` | [Open](youtube_pro_addon/README.md) |

<!-- AUTO-ADDON-CATALOG:END -->

## Updates

When a new add-on version is published:

1. Open **Settings → Add-ons → Add-on Store**.
2. Open the installed add-on.
3. Review the changelog and backup your configuration.
4. Select **Update**.
5. Test the add-on after the upgrade.

## Support

For installation questions, bug reports, and feature requests, use [GitHub Issues](https://github.com/trankhanhduy2929-beep/Duy_Home_Assistant_Addons/issues).

Before posting logs:

- Remove API keys, Proxy Keys, passwords, cookies, tokens, IP addresses, and personal prompts.
- Include the add-on version, Home Assistant version, architecture, provider, and exact error.
- Use the security reporting process for vulnerabilities. See [SECURITY.md](SECURITY.md).

## Support development

These add-ons are maintained in personal development time. Sponsorship helps fund compatibility testing, documentation, security maintenance, and future improvements.

[❤️ Sponsor on GitHub](https://github.com/sponsors/trankhanhduy2929-beep)

## License and distribution

Public repository files are licensed under the [MIT License](LICENSE). Private source code and prebuilt container images may have separate terms. See [NOTICE.md](NOTICE.md).
