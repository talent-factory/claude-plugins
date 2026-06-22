# Scheduling wiki-maintain

A distributed plugin cannot start a daemon on your machine — you schedule it. Both
recipes run a weekly unattended maintenance pass.

## crontab (Linux/macOS)

Edit your crontab (`crontab -e`) and add — adjust the path to your vault:

```cron
# Weekly wiki maintenance, Mondays 08:17
17 8 * * 1 cd /path/to/your/vault && claude -p "/wiki:maintain --auto-fix --quiet" >> "$HOME/.wiki-maintain.log" 2>&1
```

## launchd (macOS, survives reboots)

Create `~/Library/LaunchAgents/ch.talent-factory.wiki-maintain.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>ch.talent-factory.wiki-maintain</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>cd /path/to/your/vault && claude -p "/wiki:maintain --auto-fix --quiet"</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>17</integer></dict>
  <key>StandardOutPath</key><string>/tmp/wiki-maintain.out</string>
  <key>StandardErrorPath</key><string>/tmp/wiki-maintain.err</string>
</dict>
</plist>
```

Load it: `launchctl load ~/Library/LaunchAgents/ch.talent-factory.wiki-maintain.plist`

## Notes

- Use an off-minute (`:17`) rather than `:00` to avoid load spikes.
- `--quiet` exits non-zero when unresolved critical findings remain — your wrapper
  can alert on that.
