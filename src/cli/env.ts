import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import type { Command } from "commander";
import pc from "picocolors";

const CONFIG_DIR = join(homedir(), ".config", "gtm-sheets");
const ENV_FILE = join(CONFIG_DIR, ".env");

export function getGlobalEnvPath(): string {
  return ENV_FILE;
}

function ensureConfigDir(): void {
  if (!existsSync(CONFIG_DIR)) {
    mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

function readEnvFile(): Map<string, string> {
  const entries = new Map<string, string>();
  if (!existsSync(ENV_FILE)) return entries;

  const content = readFileSync(ENV_FILE, "utf-8");
  for (const line of content.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIndex = trimmed.indexOf("=");
    if (eqIndex === -1) continue;
    const key = trimmed.slice(0, eqIndex).trim();
    const value = trimmed.slice(eqIndex + 1).trim();
    entries.set(key, value);
  }
  return entries;
}

function writeEnvFile(entries: Map<string, string>): void {
  ensureConfigDir();
  const lines = Array.from(entries.entries()).map(
    ([key, value]) => `${key}=${value}`,
  );
  writeFileSync(ENV_FILE, `${lines.join("\n")}\n`, { mode: 0o600 });
}

function maskValue(value: string): string {
  if (value.length <= 8) return "****";
  return `${value.slice(0, 4)}****${value.slice(-4)}`;
}

export function registerEnv(program: Command): void {
  const env = program
    .command("env")
    .description("Manage API keys stored in ~/.config/gtm-sheets/.env");

  env
    .command("set <key=value>")
    .description("Set an environment variable")
    .action((pair: string) => {
      const eqIndex = pair.indexOf("=");
      if (eqIndex === -1) {
        console.error(
          pc.red("Invalid format. Use: gtm-sheets env set KEY=value"),
        );
        process.exit(1);
      }
      const key = pair.slice(0, eqIndex).trim();
      const value = pair.slice(eqIndex + 1).trim();
      if (!key) {
        console.error(pc.red("Key cannot be empty."));
        process.exit(1);
      }
      const entries = readEnvFile();
      const isUpdate = entries.has(key);
      entries.set(key, value);
      writeEnvFile(entries);
      console.log(
        isUpdate
          ? `${pc.green("Updated")} ${pc.bold(key)}`
          : `${pc.green("Set")} ${pc.bold(key)}`,
      );
    });

  env
    .command("remove <key>")
    .description("Remove an environment variable")
    .action((key: string) => {
      const entries = readEnvFile();
      if (!entries.has(key)) {
        console.error(pc.yellow(`${key} not found.`));
        process.exit(1);
      }
      entries.delete(key);
      writeEnvFile(entries);
      console.log(`${pc.green("Removed")} ${pc.bold(key)}`);
    });

  env
    .command("list")
    .description("List all stored environment variables (values masked)")
    .action(() => {
      const entries = readEnvFile();
      if (entries.size === 0) {
        console.log(pc.dim("No environment variables configured."));
        console.log(pc.dim(`Run: gtm-sheets env set API_KEY=your_key`));
        return;
      }
      for (const [key, value] of entries) {
        console.log(`${pc.bold(key)}=${pc.dim(maskValue(value))}`);
      }
    });

  env
    .command("path")
    .description("Print the path to the global env file")
    .action(() => {
      console.log(ENV_FILE);
    });
}
