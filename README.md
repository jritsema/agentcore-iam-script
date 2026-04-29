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

	"Harness": [
      "CreateHarness",
      "DeleteHarness",
      "GetHarness",
      "InvokeHarness",
      "ListHarnesses",
      "ListTagsForResource",
      "TagResource",
      "UntagResource",
      "UpdateHarness"
    ],
    "Tool Registry": [
      "CreateRegistry",
      "CreateRegistryRecord",
      "DeleteRegistry",
      "DeleteRegistryRecord",
      "GetRegistry",
      "GetRegistryRecord",
      "InvokeRegistryMcp",
      "ListRegistries",
      "ListRegistryRecords",
      "SearchRegistryRecords",
      "SubmitRegistryRecordForApproval",
      "UpdateRegistry",
      "UpdateRegistryRecord",
      "UpdateRegistryRecordStatus"
    ]
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
