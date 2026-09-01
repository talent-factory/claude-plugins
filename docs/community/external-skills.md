# External Skill Collections

Individual Claude Code skills you can adopt à la carte — as distinct from the [full marketplaces](external-resources.md) that ship an entire `plugin.json`-managed catalog. Collections on this page are typically installed by copying or symlinking a skill folder into `.claude/skills/` (project scope) or `~/.claude/skills/` (user scope), sometimes via a third-party installer such as `npx skills add owner/repo`. None of this flows through Claude Code's plugin/marketplace mechanism, so there is no built-in version pinning, update channel, or review gate — treat installation the way you would treat adding any third-party dependency to a project.

---

## Curated Collections

These three collections were independently confirmed to exist and match their description at the time of writing:

| Collection | Description | Repository |
|------------|-------------|------------|
| Superpowers | Process-layer skills — TDD, systematic debugging, brainstorming, code review, and worktree-based collaboration patterns that a coding agent is instructed to invoke before acting. | [obra/superpowers](https://github.com/obra/superpowers) |
| mattpocock/skills | Workflow-enforcement skills (planning, TDD, debugging, domain modeling, merge-conflict resolution) rather than raw capability extension. Ships its own script for linking selected skills instead of the whole repository. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| gstack | Garry Tan's opinionated multi-skill setup — CEO, design, eng-manager, QA, and security review personas exposed as slash commands. | [garrytan/gstack](https://github.com/garrytan/gstack) |

---

## Further Curated Lists

Beyond individual collections, third parties periodically publish broader roundups. One such list, reproduced below with its original categories, is [Charlie Hills' "22 Claude Skills for Power Users"](https://charliehills.substack.com/) (MarTech AI Newsletter, July 2026).

!!! warning "Unverified third-party content"
    Only the three entries above have been independently confirmed. The table below is reproduced from the source as-is, with popularity metrics removed because they could not be verified and looked implausible for single-purpose skill repositories. **Confirm that a repository exists, is actively maintained, and matches its description before installing anything from it.**

=== "Build"

    | Skill | Description | Repository |
    |-------|-------------|------------|
    | superpowers | Plans and debugs before it writes | [obra/superpowers](https://github.com/obra/superpowers) |
    | gstack | 23 skills in one setup | [garrytan/gstack](https://github.com/garrytan/gstack) |
    | caveman | No-fluff answers, no padding | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) |
    | ponytail | Says nothing, writes one line | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
    | codex | Runs Codex inside Claude Code | [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) |
    | i-have-adhd | Stops it burying the answer | *no public repository at time of writing* |

=== "Design"

    | Skill | Description | Repository |
    |-------|-------------|------------|
    | ui-ux-pro-max | Palettes and fonts that work | [nextlevelbuild/ui-ux-pro-max](https://github.com/nextlevelbuild/ui-ux-pro-max) |
    | taste-skill | Makes a page look expensive | [leonxlnx/taste](https://github.com/leonxlnx/taste) |
    | impeccable | The polish pass on any front end | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) |
    | hyperframes | Turns a web page into a video | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) |
    | emil | Beautiful interface animations | [emilkowalski/emil](https://github.com/emilkowalski/emil) |
    | gsap | Smooth web animations | [greensock/gsap](https://github.com/greensock/gsap) |

=== "Research"

    | Skill | Description | Repository |
    |-------|-------------|------------|
    | skill-creator | Build your own skills | [anthropics/skill-creator](https://github.com/anthropics/skill-creator) |
    | graphify | Turns notes into a map | [Graphify-Lab/graphify](https://github.com/Graphify-Lab/graphify) |
    | last30days | What the internet said this month | [mvanhorn/last30days](https://github.com/mvanhorn/last30days) |
    | agent-browser | Lets Claude use any website | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) |
    | find-skills | Finds any skill for you | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
    | claude-hud | Shows what Claude is doing live | [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud) |

=== "Marketing"

    | Skill | Description | Repository |
    |-------|-------------|------------|
    | remotion | Build full videos in React | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) |
    | marketingskills | 40 marketing skills in one pack | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
    | humanizer | Strips the AI tells from your writing | [blader/humanizer](https://github.com/blader/humanizer) |
    | social-media-skills | Charlie Hills' own content pack | [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills) |

---

## Using External Skills Without Bloating Your Context

Every installed skill's name and one-line description is loaded into the model's context on every turn, so that the model can decide whether to invoke it — this happens whether or not the skill is ever triggered. A large, indiscriminately installed collection therefore has a real, recurring token cost even on sessions that never touch it. Treat skill adoption as a curation problem, not a one-time install:

- **Prefer project scope over user scope.** Put skills in a repository's `.claude/skills/` rather than the global `~/.claude/skills/` whenever they are only relevant to that project. The token cost then only applies to sessions that actually work in that repository.
- **Cherry-pick, don't bulk-install.** From a 20+ skill pack, symlink or copy only the two or three skills you actually invoke regularly, rather than pulling in the entire collection. Several collections (including `mattpocock/skills`) ship a helper script for exactly this purpose — check the repository's `scripts/` or `README.md` before resorting to a manual copy.
- **Trial in isolation first.** Test a new skill with `claude --plugin-dir <path>` or in a disposable worktree before adding it to your global configuration, so a broken or overly broad trigger description does not affect every other session.
- **Write (or edit) trigger descriptions narrowly.** A skill's `description` frontmatter is what the model matches against; an overly broad description causes false triggers, which then pull the skill's full body into context unnecessarily.
- **Audit periodically.** Revisit `.claude/skills/` and `~/.claude/skills/` every so often and remove anything you have not invoked in months. There is no built-in expiry — unused skills persist and keep costing tokens until removed.

---

## A Note on Trust

A skill is not passive documentation — its instructions are read and acted on by the coding agent, and some collections bundle executable scripts invoked by hooks or slash commands. Review a skill's `SKILL.md` and any bundled scripts before installing it, exactly as you would review a third-party dependency's source before adding it to a project. This applies doubly to collections aggregated from many different, unrelated authors, such as the roundup above.

---

## See Also

- [External Resources](external-resources.md) - Full plugin marketplaces and MCP server directories
- [Plugin Catalog](../plugins/index.md) - Browse Talent Factory plugins
- [Skills & Agents Activation](../reference/skills-agents-activation.md) - How Claude Code decides which skill to invoke
- [Plugin Development](../development/plugin-development.md) - Create your own plugins and skills
