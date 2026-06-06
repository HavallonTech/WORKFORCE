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