# NetReact
Overview NetGuardian is an intelligent network monitoring tool that automatically detects connectivity issues and performs corrective actions on routers via SSH. It uses a two-phase monitoring approach with configurable thresholds to identify network problems and implement predefined fixes.

Key Features
Dual-Phase Monitoring:

Phase 1: Continuous ping monitoring with configurable interval

Phase 2: Intensive diagnostic mode when thresholds are exceeded

Automated Remediation: Executes predefined router commands when issues are detected

Configurable Thresholds: Adjustable timeout values for both monitoring phases

Multi-Router Support: Manages primary and secondary routers simultaneously

Source-Specific Pinging: Tests connectivity from specific router interfaces

Technical Details
Protocols: SSH for router communication

Commands: Cisco-style CLI commands (configurable for other devices)

Monitoring Method: ICMP ping with source interface specification

Error Detection: Regex-based timeout pattern matching

Use Cases
Enterprise network monitoring

ISP edge router management

Network redundancy systems

Automated network troubleshooting

Requirements
Python 3.x

Paramiko (SSH library)

Network access to routers

SSH credentials with configuration privileges

Configuration
Edit the script's config section to specify:

Router IPs and credentials

Ping targets and source interfaces

Monitoring intervals and thresholds

Remediation commands

How It Works
Continuously pings target from primary router

Enters Phase 2 if timeouts exceed threshold

Executes remediation commands on secondary router

Returns to normal monitoring when connectivity improves
