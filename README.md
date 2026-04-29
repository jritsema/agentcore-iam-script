# agentcore-iam-script

Fetches AgentCore service reference and classifies IAM actions by subservice.

## Example Output

```text
Changes since 2026-04-29T11:53:50.651634:
  + CreateHarness
  + CreateRegistry
  + CreateRegistryRecord
  + DeleteHarness
  + DeleteRegistry
  + DeleteRegistryRecord
  + GetHarness
  + GetRegistry
  + GetRegistryRecord
  + InvokeHarness
  + InvokeRegistryMcp
  + ListHarnesses
  + ListRegistries
  + ListRegistryRecords
  + SearchRegistryRecords
  + SubmitRegistryRecordForApproval
  + UpdateHarness
  + UpdateRegistry
  + UpdateRegistryRecord
  + UpdateRegistryRecordStatus

	...

## Harness (6 actions)
  Write        CreateHarness
  Write        DeleteHarness
  Read         GetHarness
  Write        InvokeHarness
  List         ListHarnesses
  Write        UpdateHarness

## Tool Registry (14 actions)
  Write        CreateRegistry
  Write        CreateRegistryRecord
  Write        DeleteRegistry
  Write        DeleteRegistryRecord
  Read         GetRegistry
  Read         GetRegistryRecord
  Read         InvokeRegistryMcp
  List         ListRegistries
  List         ListRegistryRecords
  Read         SearchRegistryRecords
  Write        SubmitRegistryRecordForApproval
  Write        UpdateRegistry
  Write        UpdateRegistryRecord
  Write        UpdateRegistryRecordStatus
```

## Development

Initialize the project:
```
make init
```

Add dependencies:
```
make install <package-name>
```

Run the project:
```
make start
```
