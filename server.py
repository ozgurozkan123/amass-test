import os
import shlex
import subprocess
from fastmcp import FastMCP

mcp = FastMCP("amass-mcp")

@mcp.tool()
def amass(
    subcommand: str,
    domain: str | None = None,
    intel_whois: bool | None = None,
    intel_organization: str | None = None,
    enum_type: str | None = None,
    enum_brute: bool | None = None,
    enum_brute_wordlist: str | None = None,
) -> str:
    """
    Advanced subdomain enumeration and reconnaissance tool powered by OWASP Amass CLI.

    Args:
        subcommand: "enum" or "intel" to select Amass mode.
        domain: Target domain (required for enum; optional for intel).
        intel_whois: Include WHOIS data when gathering intel.
        intel_organization: Organization name for intel searches.
        enum_type: "active" or "passive" enumeration mode.
        enum_brute: Whether to brute-force subdomains.
        enum_brute_wordlist: Path/URL to wordlist for brute force.
    Returns:
        Raw Amass CLI output (stdout + stderr).
    """

    if subcommand not in {"enum", "intel"}:
        raise ValueError("subcommand must be 'enum' or 'intel'")

    amass_args: list[str] = [subcommand]

    if subcommand == "enum":
        if not domain:
            raise ValueError("domain is required for enum")
        amass_args += ["-d", domain]
        if enum_type == "passive":
            amass_args.append("-passive")
        if enum_brute:
            amass_args.append("-brute")
            if enum_brute_wordlist:
                amass_args += ["-w", enum_brute_wordlist]

    if subcommand == "intel":
        if not domain and not intel_organization:
            raise ValueError("either domain or intel_organization is required for intel")
        if domain:
            amass_args += ["-d", domain]
            if intel_whois:
                amass_args.append("-whois")
        if intel_organization:
            amass_args += ["-org", intel_organization]
        if intel_whois and "-whois" not in amass_args:
            amass_args.append("-whois")

    cmd = ["amass", *amass_args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        raise RuntimeError(f"Amass exited with code {result.returncode}: {output}")
    return output.strip()


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        path="/mcp",
    )
