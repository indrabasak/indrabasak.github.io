---
layout: post
title: TLS with Spring
published: false
comments: true
tags: [TLS, Spring, Java]
  
image: /images/entry/classfile-duke.svg
---

### X.509 Certificate 

An X.509 certificate contains the public key that may be used to verify an 
end entity (EE) such as a web site. The format of the certificate is specified
in [RFC 3280: Internet X.509 Public Key Infrastructure Certificate and 
CRL Profile](http://www.ietf.org/rfc/rfc3280.txt). Here is an example of a 
X.509 certificate,

![ClassA.java](/images/tls/certificate-example.svg?style=centerme)

**Version:** This field specifies the version of the certificate.

**Serial number:** It is a unique positive integer assigned by the CA to
   each certificate.
   
**Signature :** It contains the algorithm identifier for the algorithm used
by the CA to sign the certificate.  

**Subject:**  The entity is defined in the `subject` attribute of the certificate or 
              in some cases in `subjectAltName (SAN)`. The subject comes in the 
              form of a `Distinguished Name` (DN), e.g.,

The subject field identifies the entity associated with the public
   key stored in the subject public key field.  The subject name MAY be
   carried in the subject field and/or the subjectAltName extension.  If
   the subject is a CA (e.g., the basic constraints extension, as
   discussed in 4.2.1.10, is present and the value of cA is TRUE), then
   the subject field MUST be populated with a non-empty distinguished
   name matching the contents of the issuer field (section 4.1.2.4) in
   all certificates issued by the subject CA.  If the subject is a CRL
   issuer (e.g., the key usage extension, as discussed in 4.2.1.3, is
   present and the value of cRLSign is TRUE) then the subject field MUST
   be populated with a non-empty distinguished name matching the
   contents of the issuer field (section 4.1.2.4) in all CRLs issued by
   the subject CRL issuer.  If subject naming information is present
   only in the subjectAltName extension (e.g., a key bound only to an
   email address or URI), then the subject name MUST be an empty
   sequence and the subjectAltName extension MUST be critical.

   Where it is non-empty, the subject field MUST contain an X.500
   distinguished name (DN).  The DN MUST be unique for each subject
   entity certified by the one CA as defined by the issuer name field.
   A CA MAY issue more than one certificate with the same DN to the same
   subject entity.

   The subject name field is defined as the X.501 type Name.
   Implementation requirements for this field are those defined for the
   issuer field (section 4.1.2.4).  When encoding attribute values of
   type DirectoryString, the encoding rules for the issuer field MUST be
   implemented.  Implementations of this specification MUST be prepared
   to receive subject names containing the attribute types required for
   the issuer field.  Implementations of this specification SHOULD be
   prepared to receive subject names containing the recommended
   attribute types for the issuer field.  The syntax and associated
   object identifiers (OIDs) for these attribute types are provided in
   the ASN.1 modules in Appendix A.  Implementations of this
   specification MAY use these comparison rules to process unfamiliar
   attribute types (i.e., for name chaining).  This allows
   implementations to process certificates with unfamiliar attributes in
   the subject name.

   In addition, legacy implementations exist where an RFC 822 name is
   embedded in the subject distinguished name as an EmailAddress
   attribute.  The attribute value for EmailAddress is of type IA5String
   to permit inclusion of the character '@', which is not part of the
   PrintableString character set.  EmailAddress attribute values are not
   case sensitive (e.g., "fanfeedback@redsox.com" is the same as
   "FANFEEDBACK@REDSOX.COM").



Housley, et. al.            Standards Track                    [Page 23]

RFC 3280        Internet X.509 Public Key Infrastructure      April 2002


   Conforming implementations generating new certificates with
   electronic mail addresses MUST use the rfc822Name in the subject
   alternative name field (section 4.2.1.7) to describe such identities.
   Simultaneous inclusion of the EmailAddress attribute in the subject
   distinguished name to support legacy implementations is deprecated
   but permitted.



The entity is defined in the subject attribute of the certificate or, increasingly, in the . The subject is described in the form of a Distinguished Name (DN) - backgrounder about DN/RDNs in LDAP - which is comprised of a number of Relative Distinguished Names (RDNs) each of which is a data-containing element called an Attribute. Specifically, the CN (commonName) attribute (RDN) of the Distinguished Name typically contains the end-entity covered by the certificate. An example of a CN may be a web site address such as CN=www.example.com. A full subject or subjectaltName DN may contain one or more of the following RDNs CN= (commonName, the end-entity being covered, example, a website or www.example.com), C= (country), ST= (state or province within country), L= (location , nominally an address but ambiguously used except in EV certificates where it is rigorously defined), OU= (organizationalUnitName, a company division name or similar sub-structure), O= (organizationName, typically a company name).