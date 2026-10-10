# AddInTemplate

AddInTemplate is the starting point for writing your own Autodesk Fusion 360 add-in.
It has two parts:

- a **demo add-in** (`apps/desktop-template/AddInTemplate`) with one command, a translated dialog, a live preview and input checks
- a **scaffolding script** (`tools/template/new_addin.py`) that copies the demo add-in and renames everything that must be unique

| Fact | Value |
| --- | --- |
| Version | 1.0.0.0 |
| Release ZIP | none for this version – it is used from the repository |
| Works on | Windows and macOS (manifest: `windows\|mac`) |
| Interface languages | German, English, Spanish, French, Italian |
| Dependencies | none – Python standard library only |
| Licence | MIT |
| Author | Sorglos Thomas Weirich |
| Repository | <https://github.com/sorglos-it/fusion360> |

## Contents

| File | What you find there |
| --- | --- |
| [installation.md](installation.md) | Requirements, getting the repository, creating a new add-in, Fusion's add-in folder, first start, removal |
| [usage.md](usage.md) | What the demo command does, and how to turn the copy into your own add-in |
| [settings.md](settings.md) | Everything you set in the entry file, in the manifest and in the language files |
| [how-it-works.md](how-it-works.md) | Entry file, core module, handler registry, event flow, text catalogue |
| [troubleshooting.md](troubleshooting.md) | Every message, its cause and what to do; known pitfalls |
| [development.md](development.md) | Folders, offline check, icon tool, version numbers, packing, decisions |

## Good to know before you start

- Every add-in created from the template gets its **own copy** of the core module. A fix made in the template later does **not** reach add-ins created earlier.
- The offline check was run for this documentation and passed. The behaviour inside Fusion 360 is described from the code; it was **not tested in Fusion** for this documentation.

Other languages: [language list](../index.md)
