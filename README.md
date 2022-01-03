# Benchmark Control Mapper
#### Video Demo:  <URL HERE>
#### Description:

Security Control Assessors (SCAs) are responsible for the hardening and security of systems.
To determine if a system is secure they must scan the system against checks that have been created and documented in a Benchmark.
Generally speaking, each check in a Benchmark correlates to one or more National Institute of Standards and Technology (NIST) 800-53 controls.
These controls however are not individually mapped inside the Benchmark. The Benchmark aligns checks to Common Control Identifiers (CCIs) which are mapped to NIST 800-53 controls.

Currently, an SCA would need to look at the CCI control inside of a check and then cross reference that value with its mapped NIST Control.
While this is not a hard task, it is a tedious one that eats away at the time someone has to complete the documentation of hardening of a system.

My application is meant to bridge the divide between the Benchmark and the NIST Controls each check is associated with.
It uses Python, Django REST API, PostgreSQL, and Angular to parse and store benchmarks and give the user a quick look at all of the checks present and their mapped CCIs and NIST Controls.
Users can also plainly view CCI to NIST (or CCI to NIST) mappings without having a Benchmark already present.

The application is set up and deployed using Docker, which makes it easier for an SCA who may not have the technical expertise to manage the application.