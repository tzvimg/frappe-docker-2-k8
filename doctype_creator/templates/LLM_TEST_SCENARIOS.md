# LLM Generation Test Scenarios

This document contains test scenarios for validating that LLMs can successfully generate valid DocType YAML specifications using the prompt template.

## Test Scenario 1: Simple Master Data

**User Request:**
> I need a DocType for tracking equipment in our nursing facilities. Each equipment item should have a name, serial number, purchase date, and status (Available, In Use, Under Maintenance, Retired).

**Expected YAML Structure:**
- DocType name: "Equipment"
- Module: "Nursing Management"
- Auto-naming: "format:EQ-{#####}"
- Fields:
  - equipment_name (Data, required)
  - serial_number (Data, unique)
  - purchase_date (Date)
  - status (Select with 4 options)
  - Basic section breaks

**Validation Points:**
- ✅ All fieldnames are snake_case
- ✅ Labels are in Hebrew
- ✅ Serial number marked as unique
- ✅ Status has proper Hebrew options
- ✅ Proper naming rule
- ✅ Permissions defined

## Test Scenario 2: DocType with Relationships

**User Request:**
> Create a DocType for Patient Care Plans. Each care plan should be linked to a specific caregiver and include start date, end date, care type (Home Care, Day Center, Community Support), daily hours needed, and special instructions.

**Expected YAML Structure:**
- DocType name: "Patient Care Plan" or "Care Plan"
- Link to Caregiver DocType
- Link to Service Provider (optional)
- Date range fields (start_date, end_date)
- Select field for care_type
- Float field for daily_hours
- Text field for special_instructions
- Sections for organization

**Validation Points:**
- ✅ Link fields have correct options
- ✅ Care type options in Hebrew
- ✅ Float field has precision
- ✅ Text field used for long content
- ✅ Auto-fetch caregiver name
- ✅ Fields organized into sections

## Test Scenario 3: Workflow-Based DocType

**User Request:**
> I need a DocType for Leave Requests. Employees submit requests with start date, end date, leave type (Vacation, Sick Leave, Personal), and reason. It should go through an approval workflow with states: Draft, Pending Manager Approval, Approved, Rejected.

**Expected YAML Structure:**
- DocType name: "Leave Request"
- is_submittable: true
- Fields:
  - start_date, end_date
  - leave_type (Select)
  - reason (Text)
  - workflow_state (Select, read_only)
  - approved_by (Link to User, read_only)
  - approval_date (Datetime, read_only)
  - rejection_reason (Text)
- Permissions for different roles

**Validation Points:**
- ✅ is_submittable set to true
- ✅ Workflow state is read_only
- ✅ Approval fields are read_only
- ✅ Different permissions for submitters vs approvers
- ✅ Leave type options in Hebrew
- ✅ Proper section organization

## Test Scenario 4: DocType with Child Table

**User Request:**
> Create a Training Session DocType. Each session has a title, date, location, and instructor. It should also track attendees with their attendance status (Present, Absent, Excused).

**Expected YAML Structure:**
- DocType name: "Training Session"
- Parent fields: title, session_date, location, instructor
- Child table field: attendees
  - References child DocType "Training Attendee"
- Proper sections

**Note:** Child DocType would need to be created separately with:
- istable: 1
- Fields: attendee (Link to User/Caregiver), status (Select)

**Validation Points:**
- ✅ Table field has correct child DocType in options
- ✅ Clear that child DocType needs separate creation
- ✅ Parent fields well organized
- ✅ Attendance status in Hebrew

## Test Scenario 5: Complex Relationships with Auto-Fetch

**User Request:**
> I need a DocType for Service Delivery Records. Each record should link to a Service Provider, automatically show the provider's name and HP number, link to a Branch (from that provider), link to a Caregiver, show the caregiver's name and ID, include service date, hours provided, and notes.

**Expected YAML Structure:**
- DocType name: "Service Delivery Record"
- Links:
  - service_provider (Link)
  - provider_name (auto-fetched, read_only)
  - hp_number (auto-fetched, read_only)
  - branch (Link)
  - caregiver (Link)
  - caregiver_name (auto-fetched, read_only)
  - caregiver_id (auto-fetched, read_only)
- Data fields:
  - service_date (Date)
  - hours_provided (Float)
  - notes (Text)

**Validation Points:**
- ✅ Multiple Link fields with correct options
- ✅ Auto-fetched fields marked read_only
- ✅ fetch_from syntax correct
- ✅ Float field has precision
- ✅ Good section organization
- ✅ Key fields in list view

## Test Scenario 6: Master Data with Status Tracking

**User Request:**
> Create a Facility DocType for tracking nursing facilities. Include facility name, address, facility type (Home Care, Day Center, Residential), capacity (number of beds), manager name, phone, email, license number (should be unique), license expiry date, and status (Active, Inactive, Pending License).

**Expected YAML Structure:**
- DocType name: "Facility"
- Basic fields: name, address
- Select: facility_type, status
- Int: capacity
- Contact fields: manager_name, phone, email
- License fields: license_number (unique), license_expiry
- Sections: Basic Info, Contact, License, Status

**Validation Points:**
- ✅ License number marked unique
- ✅ Appropriate field types (Int for capacity)
- ✅ Email field has options: "Email"
- ✅ Phone field has options: "Phone"
- ✅ All Hebrew labels
- ✅ Status in list view
- ✅ License expiry shown (important date)

## Test Scenario 7: Configuration/Settings DocType

**User Request:**
> I need a Settings DocType for system-wide configuration. It should have default service hours per week, default hourly rate, enable/disable automatic notifications, notification email address, and grace period in days for document expiry warnings.

**Expected YAML Structure:**
- DocType name: "System Settings" or "Nursing Settings"
- Single DocType (only one instance) - note in comments
- Fields:
  - default_weekly_hours (Float)
  - default_hourly_rate (Float)
  - enable_notifications (Check)
  - notification_email (Data with Email option)
  - expiry_grace_days (Int)

**Validation Points:**
- ✅ Check fields for toggles
- ✅ Float fields with precision
- ✅ Int for day count
- ✅ Email field properly configured
- ✅ Sensible defaults
- ✅ Clear field descriptions

## Test Scenario 8: Minimum Viable DocType

**User Request:**
> Quick DocType for tracking complaints. Just need a title, complaint date, description, and status (New, In Progress, Resolved).

**Expected YAML Structure:**
- DocType name: "Complaint"
- Minimal fields (only what's requested)
- Simple structure
- Basic permissions

**Validation Points:**
- ✅ No unnecessary fields added
- ✅ All required fields present
- ✅ Status with Hebrew options
- ✅ Default date to Today
- ✅ Simple, clean structure
- ✅ Appropriate field types

## Test Scenario 9: DocType with Calculated Fields

**User Request:**
> Create a Timesheet DocType. Link to a caregiver, link to a service provider, date, start time, end time, hourly rate. Should calculate total hours and total payment automatically.

**Expected YAML Structure:**
- DocType name: "Timesheet"
- Links: caregiver, service_provider
- Time fields: date, start_time, end_time
- Rate: hourly_rate (Float)
- Calculated (read_only): total_hours (Float), total_payment (Float)
- Clear note that calculations need Python controller

**Validation Points:**
- ✅ Calculated fields marked read_only
- ✅ Description mentions automatic calculation
- ✅ Comment about Python controller needed
- ✅ Float fields have proper precision
- ✅ Datetime fields used appropriately

## Test Scenario 10: Edge Cases and Clarifications

**User Request:**
> I need a DocType for... actually, I'm not sure. Something to track service provider performance metrics.

**Expected LLM Behavior:**
Should ask clarifying questions:
- What specific metrics do you want to track? (quality scores, response time, etc.)
- Should this link to Service Provider DocType?
- Who will enter this data?
- How often is this measured?
- What time period does each record cover?
- Are there standard performance indicators or custom ones?

**Validation Points:**
- ✅ LLM asks clarifying questions
- ✅ Waits for answers before generating
- ✅ Doesn't make too many assumptions
- ✅ Final YAML matches clarified requirements

## LLM Prompt Testing Checklist

When testing LLM generation with the prompt template:

### Input Quality
- [ ] Test with clear, well-defined requirements
- [ ] Test with vague requirements (should ask questions)
- [ ] Test with conflicting requirements (should clarify)
- [ ] Test with Hebrew terminology mixed in
- [ ] Test with business domain language

### Output Quality
- [ ] All fieldnames are snake_case
- [ ] All labels are in Hebrew
- [ ] Field types appropriate for data
- [ ] Required fields marked properly
- [ ] Unique fields marked properly
- [ ] Sections used for organization
- [ ] Column breaks used appropriately
- [ ] Link fields have correct options
- [ ] Select fields have Hebrew options
- [ ] Naming rule is sensible
- [ ] Permissions are appropriate
- [ ] Description is clear

### Validation Compatibility
- [ ] Generated YAML passes schema validation
- [ ] No reserved fieldnames used
- [ ] No duplicate fieldnames
- [ ] Options provided for Select/Link/Table
- [ ] Labels provided for data fields
- [ ] Proper indentation (2 spaces)
- [ ] Valid YAML syntax

### Best Practices Adherence
- [ ] Fields organized logically
- [ ] 3-5 fields in list view
- [ ] Important fields in filters
- [ ] Read-only fields marked
- [ ] Sensible defaults provided
- [ ] Field descriptions for complex fields
- [ ] No over-engineering
- [ ] Follows patterns from examples

## Example LLM Conversations

### Example 1: Successful Generation

**User:** Create a DocType for tracking medical equipment inventory.

**LLM:** I'll help you create a medical equipment inventory DocType. Let me ask a few clarifying questions:

1. What key information do you need for each equipment item?
2. Should this link to facilities or service providers?
3. Do you need to track maintenance schedules?
4. What status values do you need (Available, In Use, etc.)?

**User:** Just basic info: equipment name, type (Bed, Wheelchair, Oxygen Tank, Walker), serial number, purchase date, status (Available, In Use, Under Maintenance, Retired). Link to facility would be good.

**LLM:** Perfect! Here's the YAML specification:

```yaml
doctype:
  name: "Medical Equipment"
  module: "Nursing Management"
  naming_rule: "autoname"
  autoname: "format:MED-{#####}"
  track_changes: true
  description: "Medical equipment inventory tracking"
  # ... complete valid YAML
```

### Example 2: Needs Clarification

**User:** Make a DocType for tracking stuff.

**LLM:** I'd be happy to help create a DocType, but I need more information:

1. What kind of "stuff" are you tracking? (documents, equipment, supplies, etc.)
2. What information do you need to record about each item?
3. Who will be using this DocType?
4. Does this relate to any existing DocTypes in your system?

Could you provide more details about your requirements?

## Success Metrics

A successful LLM generation should:

1. **Pass validation**: `python validate_yaml.py` returns no errors
2. **Load successfully**: `python load_doctype.py` creates the DocType
3. **Match intent**: Fulfills user's stated requirements
4. **Follow conventions**: Uses Hebrew labels, proper naming, etc.
5. **Be maintainable**: Clear structure, well-organized
6. **Be practical**: No over-engineering, sensible defaults

## Common LLM Mistakes to Watch For

1. **Using camelCase for fieldnames** → Should be snake_case
2. **English labels** → Should be Hebrew
3. **Forgetting options for Select** → Always required
4. **Wrong field types** → Data for numbers, Text for single line
5. **No sections** → Should organize with Section Breaks
6. **Reserved fieldnames** → Avoid 'name', 'owner', etc.
7. **Missing permissions** → Always define at least System Manager
8. **Too many assumptions** → Should ask clarifying questions

## Iteration and Refinement

If initial generation isn't perfect:

1. Identify specific issues (wrong field type, missing section, etc.)
2. Provide corrective feedback
3. Regenerate or edit specific parts
4. Validate again
5. Repeat until satisfactory

The goal is for 80% of generations to be usable with minimal editing.
