Phase 1 Goal, Unir has been renamed Project
Units remaned to Project
MySQL database auto-created if it doesn't exist
Tables auto-created
Super Admin auto-created if none exists
Login page
Dashboard page
Flask-Login authentication
Modular structure ready for Attendance, GPS Tracking, Leave Management, etc.

Username: superadmin
Password: Admin@123
bthddzow_workforceport
bthddzow_kplanet_1
+gz9K?KTZkj;y=X2

Live Server
superadmin
Admin@123

python -m pip install pandas openpyxl reportlab

Attendance Interpretation A:
Staff clocks in every hour:

08:00 AM  Punch 1
09:00 AM  Punch 2
10:00 AM  Punch 3
11:00 AM  Punch 4
12:00 PM  Punch 5
01:00 PM  Punch 6
02:00 PM  Punch 7
03:00 PM  Punch 8

User can mark attendance
8 times daily.

System blocks attendance
after 8 entries.

Office Staff
→ Use Check In / Check Out

Field Marketers
→ Use Attendance Punches (8 Punches)

Assigned to Campaign A
↓
Assigned to Unit/Location
↓
Must prove presence periodically
↓
GPS + Selfie + Timestamp




Lock Down The Business Rules

Field marketers are assigned to a unit/location.

They must prove presence periodically.

Rule 1: Attendance Window

Should attendance be allowed only during:
08:00 AM - 05:00 PM
Rule 2: Maximum Checkpoints
8 checkpoints per day

Example:

Checkpoint 1
Checkpoint 2
Checkpoint 3
Checkpoint 4
Checkpoint 5
Checkpoint 6
Checkpoint 7
Checkpoint 8
Rule 3: Minimum Interval

Recommended:

60 minutes

between checkpoints.

Otherwise:

08:00 AM  Checkpoint 1
08:01 AM  Checkpoint 2
08:02 AM  Checkpoint 3
...

which defeats the purpose.

Rule 4: GPS Mandatory

Use your existing:

distance_in_meters()

logic.

Rule 5: Geofence Mandatory

Must be inside assigned location radius.

Rule 6: Selfie Mandatory

No selfie.

No checkpoint.

Rule 7: Auto Numbering

The system automatically calculates:

Design steps
Checkpoint 1 Window

Opens: 07:30 AM
Closes: 08:20 AM (Nigerian Time)

Punch 1  = 07:30 - 08:20
Punch 2  = 08:50 - 09:20
Punch 3  = 09:50 - 10:20
Punch 4  = 10:50 - 11:20
Punch 5  = 11:50 - 12:20
Punch 6  = 12:50 - 01:20
Punch 7  = 01:50 - 02:20
Punch 8  = 02:50 - 03:20







Core Features
1. User Authentication
Login with username/email and password
Role-based access:
Employee
Supervisor
HR/Admin
Super Admin
2. Attendance Management
Clock In
Clock Out
Break Start
Break End
Attendance History
3. GPS Location Tracking

When an employee clocks in:

Capture GPS coordinates
Record timestamp
Store:
Latitude
Longitude
Accuracy
Device information

Example:

Staff	Date	Check-In	Latitude	Longitude
John Doe	06-06-2026	08:03 AM	9.0765	7.3986
4. Geofencing

Restrict attendance to approved locations.

Example:

Site	Radius
Head Office	100m
Kubwa Center	150m
Wuse Center	150m

If a user is outside the approved radius:

Reject attendance, or
Mark as "Outside Geofence"
5. Live Staff Location

Supervisors can view:

Last known location
Time of last update
Online/Offline status
6. Attendance Dashboard

Statistics:

Present today
Absent today
Late arrivals
Staff currently on-site
Attendance trends
7. Reports

Generate:

Daily attendance
Monthly attendance
Late arrivals
Absenteeism
Location compliance

Export to:

Excel
PDF
CSV
8. Leave Management (Optional)
Annual leave
Sick leave
Casual leave
Approval workflow
9. Mobile App / PWA

The location feature works best through:

Android App
Progressive Web App (PWA)

The browser requests GPS permission and submits coordinates during attendance actions.


Selfie Verification

Capture a selfie during check-in to reduce buddy punching.

QR Code Attendance

Place a QR code at each site:

Scan QR code
Verify location
Mark attendance
Supervisor Approval

For staff working outside approved locations:

Attendance marked pending
Supervisor approves or rejects
Route Tracking

For field staff:

Periodic GPS updates every 5–15 minutes
Route history on map

Future Modules Under WorkForce

Phase 1 – Attendance
User Management
Clock In/Out
GPS Location Verification
Attendance Reports
Geofencing
Phase 2 – Leave Management
Annual Leave
Sick Leave
Casual Leave
Leave Approval Workflow
Phase 3 – Field Staff Management
Live Location Tracking
Route History
Site Visits
Supervisor Monitoring
Phase 4 – HR Management
Staff Records
Departments
Designations
Employment History
Phase 5 – Payroll Integration
Attendance-Based Payroll
Overtime Calculation
Monthly Reports