# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.106] - 2024-02-26

### Added

- **💡 Tooltips Added**: Tooltips have now been implemented on UI elements for enhanced guidance.

### Changed

- **🆕 Fresh New Design**: We've implemented design updates to rejuvenate our user interface.

## [0.1.105] - 2024-02-25

### Added

- **📄 Document Selection**: Now you can select and delete multiple documents at once for easier management.

### Changed

- **🏷️ Document Pre-tagging**: Simply click the "+" button at the top, enter tag names in the popup window, or select from a list of existing tags. Then, upload files with the added tags for streamlined organization.

## [0.1.104] - 2024-02-25

### Added

- **🔄 Check for Updates**: Keep your system current by checking for updates conveniently located in Settings > About.
- **🗑️ Automatic Tag Deletion**: Unused tags on the sidebar will now be deleted automatically with just a click.

### Changed

- **🎨 Modernized Styling**: Enjoy a refreshed look with updated styling for a more contemporary experience.

## [0.1.103] - 2024-02-25

### Added

- **🔗 Built-in LiteLLM Proxy**: Now includes LiteLLM proxy within Open WebUI for enhanced functionality.

  - Easily integrate existing LiteLLM configurations using `-v /path/to/config.yaml:/app/backend/data/litellm/config.yaml` flag.
  - When utilizing Docker container to run Open WebUI, ensure connections to localhost use `host.docker.internal`.

- **🖼️ Image Generation Enhancements**: Introducing Advanced Settings with Image Preview Feature.
  - Customize image generation by setting the number of steps; defaults to A1111 value.

### Fixed

- Resolved issue with RAG scan halting document loading upon encountering unsupported MIME types or exceptions (Issue #866).

### Changed

- Ollama is no longer required to run Open WebUI.
- Access our comprehensive documentation at [Open WebUI Documentation](https://docs.openwebui.com/).

## [0.1.102] - 2024-02-22

### Added

- **🖼️ Image Generation**: Generate Images using the AUTOMATIC1111/stable-diffusion-webui API. You can set this up in Settings > Images.
- **📝 Change title generation prompt**: Change the prompt used to generate titles for your chats. You can set this up in the Settings > Interface.
- **🤖 Change embedding model**: Change the embedding model used to generate embeddings for your chats in the Dockerfile. Use any sentence transformer model from huggingface.co.
- **📢 CHANGELOG.md/Popup**: This popup will show you the latest changes.

## [0.1.101] - 2024-02-22

### Fixed

- LaTex output formatting issue (#828)

### Changed

- Instead of having the previous 1.0.0-alpha.101, we switched to semantic versioning as a way to respect global conventions.
