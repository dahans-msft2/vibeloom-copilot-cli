---
artifact_id: system
artifact_type: system
tier: system-specs
scope_kind: root
scope_id: root
status: draft
version: 0
draft_revision: 1
derives_from: []
---

# System

Flat system specification for vibe mode. Covers system context, containers, components, interfaces, and behaviors in one document. On upgrade to pm/dev/expert, this document is expanded into the full system-specs tier: `system`, `containers`, per-container `container`, and per-component `component`.

## System Purpose And Context

<What the system does, who it serves, and what it interacts with.>
<!--
Exemplar:
A workspace collaboration platform that manages invitations, access control, and collaborator lifecycle. It exposes a web UI for human users and integrates with an external email delivery service for notifications.
-->

## External Actors And Systems

| id | kind | name | relationship | derives_from |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific actors.
| `EXT-0001` | `actor` | Workspace Owner | Creates workspaces, sends invitations, manages collaborators | `CAP-0001` |
| `EXT-0002` | `external-system` | Email Service | Delivers invitation notifications | `CAP-0001` |
-->

## Container Inventory

| id | container_slug | responsibility | runtime | derives_from |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific containers.
| `CONT-0001` | `app` | Web application serving UI and API | Node.js | `CAP-0001, CAP-0002` |
| `CONT-0002` | `notifications` | Sends email notifications via external service | Node.js worker | `CAP-0001` |
-->

## Communication Paths

| id | from | to | protocol | purpose |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific paths.
| `EDGE-0001` | `CONT-0001` | `CONT-0002` | async queue | Dispatch invitation notification jobs |
| `EDGE-0002` | `CONT-0002` | `EXT-0002` | HTTPS | Deliver email via external service API |
-->

## Component Inventory

| id | container_id | folder | responsibility | derives_from |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific components.
| `CMP-0001` | `CONT-0001` | `src/invite-lifecycle` | Manages invitation creation, acceptance, decline, and revocation | `CAP-0001` |
| `CMP-0002` | `CONT-0001` | `src/workspace` | Manages workspace creation and membership | `CAP-0001` |
| `CMP-0003` | `CONT-0002` | `src/email-sender` | Formats and dispatches invitation emails | `CAP-0001` |
-->

## Interfaces And Behaviors

| id | component_id | kind | description | derives_from |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific interfaces and behaviors.
| `IF-0001` | `CMP-0001` | `command` | CreateInvitation — creates a pending invitation for a target email | `CAP-0001` |
| `IF-0002` | `CMP-0001` | `event` | InvitationAccepted — emitted when a collaborator accepts | `CAP-0002` |
| `BEH-0001` | `CMP-0001` | `behavior` | An invitation must not grant access until explicitly accepted | `CST-0001` |
| `BEH-0002` | `CMP-0001` | `behavior` | Revoking an accepted invitation removes collaborator access | `CAP-0001` |
-->
