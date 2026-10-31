applyTo: '*/*'
---
Elparadisogonzalo Project Context
Project Type: Web3 dApp (Ethereum + BSC, L2/zk future)
Domain: elparadisogonzalo.com (Unstoppable Domains)
Hosting: IPFS with DNSLink + UD integration
Wallet: 0x802ba6a112f4a7bbbc2d63c8ef4bc14dfcbe6245 (EVM-compatible)
Smart Contracts: Solidity, deployed on Ethereum + BSC test/mainnet
Infrastructure:

Local Geth node (1.15.5-stable, Termux on Android)

Infura & JSON-RPC endpoints

Google Cloud CLI for backend & CI/CD automation
Frontend: React (Vite + Tailwind), ethers.js, MetaMask integration
Backend: Node.js + Web3.js, API layer for blockchain interactions
Monorepo Structure:

perl
Copy
Edit
packages/
 ├─ frontend/       # dApp UI
 ├─ backend/        # API & server logic
 ├─ contracts/      # Solidity smart contracts
 └─ my-npm-package/ # Shared utilities
Primary Goals:

Fully automated CI/CD: GitHub → IPFS → UD DNSLink update

Secure wallet interaction from frontend

Multi-chain support

zk/L2 scaling readiness

Open-source developer-friendly repo

AI Coding Guidelines
When generating, reviewing, or modifying code:

1. Code Style
Language: JavaScript/TypeScript (frontend/backend), Solidity (contracts), Bash/Shell (automation), Python (data scripts)

Formatting: Follow Prettier defaults, 2-space indentation

Naming: Use camelCase for variables/functions, PascalCase for React components, UPPER_CASE for constants

Comments:

Explain complex logic

Document all public functions in contracts and APIs

Imports: Absolute imports for shared modules (@/utils), relative imports for local files

2. Security
Never hardcode private keys — load from .env or secure vault

Validate all user inputs before sending to blockchain

Avoid inline wallet calls in React state updates — always handle in async function with error handling

Use try/catch around all Web3 calls

3. Smart Contracts
Version: Solidity ^0.8.x

Patterns: Use OpenZeppelin contracts where possible

Include:

solidity
Copy
Edit
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
Testing: Hardhat + Mocha/Chai, cover edge cases

Deployment: Scripts should support both Infura RPC and local Geth

4. Frontend
React functional components with hooks

MetaMask connection logic in a dedicated hook (useWallet.js)

All blockchain calls via ethers.js, never directly in UI components

TailwindCSS for styling; avoid inline CSS unless dynamic

5. Backend
Node.js + Express for API endpoints

ethers.js for contract calls

.env for all credentials

Include request validation & rate limiting

6. Automation & CI/CD
GitHub Actions for:

Contract compile & test

Build frontend

Upload to IPFS (Pinata or Web3.Storage)

Update UD DNSLink

Fail-fast principle: stop pipeline on first error

7. Documentation
Maintain README.md in each package

GitHub Wiki for:

Setup

Deployment

API Reference

Security Guidelines

8. AI Answering Rules
When answering questions:

Always consider Web3 context (MetaMask, ethers.js, Solidity, IPFS, UD)

Prefer step-by-step instructions

Provide working, tested code when possible

Flag potential security risks if they exist

S
