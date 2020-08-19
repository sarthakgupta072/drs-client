from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Type(Enum):
    s3 = 's3'
    gs = 'gs'
    ftp = 'ftp'
    gsiftp = 'gsiftp'
    globus = 'globus'
    htsget = 'htsget'
    https = 'https'
    file = 'file'


class AccessURL(BaseModel):
    headers: Optional[List[str]] = Field(
        None,
        description='An optional list of headers to include in the HTTP request to `url`. These headers can be used to provide auth tokens required to fetch the object bytes.',
    )
    url: str = Field(
        ...,
        description='A fully resolvable URL that can be used to fetch the actual object bytes.',
    )


class Checksum(BaseModel):
    checksum: str = Field(
        ..., description='The hex-string encoded checksum for the data'
    )
    type: str = Field(
        ...,
        description="The digest method used to create the checksum.\n\nThe value (e.g. `sha-256`) SHOULD be listed as `Hash Name String` in the https://www.iana.org/assignments/named-information/named-information.xhtml#hash-alg[IANA Named Information Hash Algorithm Registry]. Other values MAY be used, as long as implementors are aware of the issues discussed in https://tools.ietf.org/html/rfc6920#section-9.4[RFC6920].\n\nGA4GH may provide more explicit guidance for use of non-IANA-registered algorithms in the future. Until then, if implementors do choose such an algorithm (e.g. because it's implemented by their storage provider), they SHOULD use an existing standard `type` value such as `md5`, `etag`, `crc32c`, `trunc512`, or `sha1`.",
    )


class ContentsObject(BaseModel):
    contents: Optional[List[ContentsObject]] = Field(
        None,
        description='If this ContentsObject describes a nested bundle and the caller specified "?expand=true" on the request, then this contents array must be present and describe the objects within the nested bundle.',
    )
    drs_uri: Optional[List[str]] = Field(
        None,
        description='A list of full DRS identifier URI paths that may be used to obtain the object. These URIs may be external to this DRS instance.',
    )
    id: Optional[str] = Field(
        None,
        description='A DRS identifier of a `DrsObject` (either a single blob or a nested bundle). If this ContentsObject is an object within a nested bundle, then the id is optional. Otherwise, the id is required.',
    )
    name: str = Field(
        ...,
        description='A name declared by the bundle author that must be used when materialising this object, overriding any name directly associated with the object itself. The name must be unique with the containing bundle. This string is made up of uppercase and lowercase letters, decimal digits, hypen, period, and underscore [A-Za-z0-9.-_]. See http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_282[portable filenames].',
    )


class Error(BaseModel):
    msg: Optional[str] = Field(None, description='A detailed error message.')
    status_code: Optional[int] = Field(
        None,
        description='The integer representing the HTTP status code (e.g. 200, 404).',
    )


class AccessMethod(BaseModel):
    access_id: Optional[str] = Field(
        None,
        description='An arbitrary string to be passed to the `/access` method to get an `AccessURL`. This string must be unique within the scope of a single object. Note that at least one of `access_url` and `access_id` must be provided.',
    )
    access_url: Optional[AccessURL] = None
    region: Optional[str] = Field(
        "",
        description='Name of the region in the cloud service provider that the object belongs to.',
    )
    type: Type = Field(..., description='Type of the access method.')


class AccessPostMethod(BaseModel):
    access_url: Optional[AccessURL] = None
    region: Optional[str] = Field(
        "",
        description='Name of the region in the cloud service provider that the object belongs to.',
    )
    type: Type = Field(..., description='Type of the access method.')


class DrsObject(BaseModel):
    access_methods: Optional[List[AccessMethod]] = Field(
        None,
        description='The list of access methods that can be used to fetch the `DrsObject`.\nRequired for single blobs; optional for bundles.',
    )
    aliases: Optional[List[str]] = Field(
        [],
        description='A list of strings that can be used to find other metadata about this `DrsObject` from external metadata sources. These aliases can be used to represent secondary accession numbers or external GUIDs.',
    )
    checksums: List[Checksum] = Field(
        ...,
        description='The checksum of the `DrsObject`. At least one checksum must be provided.\nFor blobs, the checksum is computed over the bytes in the blob.\n\nFor bundles, the checksum is computed over a sorted concatenation of the checksums of its top-level contained objects (not recursive, names not included). The list of checksums is sorted alphabetically (hex-code) before concatenation and a further checksum is performed on the concatenated checksum value.\n\nFor example, if a bundle contains blobs with the following checksums:\nmd5(blob1) = 72794b6d\nmd5(blob2) = 5e089d29\n\nThen the checksum of the bundle is:\nmd5( concat( sort( md5(blob1), md5(blob2) ) ) )\n= md5( concat( sort( 72794b6d, 5e089d29 ) ) )\n= md5( concat( 5e089d29, 72794b6d ) )\n= md5( 5e089d2972794b6d )\n= f7a29a04',
    )
    contents: Optional[List[ContentsObject]] = Field(
        "",
        description='If not set, this `DrsObject` is a single blob.\nIf set, this `DrsObject` is a bundle containing the listed `ContentsObject` s (some of which may be further nested).',
    )
    created_time: datetime = Field(
        ...,
        description='Timestamp of content creation in RFC3339.\n(This is the creation time of the underlying content, not of the JSON object.)',
    )
    description: Optional[str] = Field(
        "", description='A human readable description of the `DrsObject`.'
    )
    id: str = Field(..., description='An identifier unique to this `DrsObject`.')
    mime_type: Optional[str] = Field(
        "", description='A string providing the mime-type of the `DrsObject`.'
    )
    name: Optional[str] = Field(
        "",
        description='A string that can be used to name a `DrsObject`.\nThis string is made up of uppercase and lowercase letters, decimal digits, hypen, period, and underscore [A-Za-z0-9.-_]. See http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_282[portable filenames].',
    )
    self_uri: str = Field(
        ...,
        description='A drs:// hostname-based URI, as defined in the DRS documentation, that tells clients how to access this object.\nThe intent of this field is to make DRS objects self-contained, and therefore easier for clients to store and pass around.  For example, if you arrive at this DRS JSON by resolving a compact identifier-based DRS URI, the `self_uri` presents you with a hostname and properly encoded DRS ID for use in subsequent `access` endpoint calls.',
    )
    size: int = Field(
        ...,
        description='For blobs, the blob size in bytes.\nFor bundles, the cumulative size, in bytes, of items in the `contents` field.',
    )
    updated_time: Optional[datetime] = Field(
        None,
        description='Timestamp of content update in RFC3339, identical to `created_time` in systems that do not support updates. (This is the update time of the underlying content, not of the JSON object.)',
    )
    version: Optional[str] = Field(
        "",
        description='A string representing a version.\n(Some systems may use checksum, a RFC3339 timestamp, or an incrementing version number.)',
    )


class PostDrsObject(BaseModel):
    name: Optional[str] = Field(
        "",
        description='A string that can be used to name a `DrsObject`.\nThis string is made up of uppercase and lowercase letters, decimal\ndigits, hyphen, period, and underscore [A-Za-z0-9.-_]. See\nhttp://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_282[portable filenames].',
    )
    description: Optional[str] = Field(
        "", description='A human readable description of the `DrsObject`.'
    )
    created_time: datetime = Field(
        ...,
        description='Timestamp of content creation in RFC3339.\n(This is the creation time of the underlying content, not of the JSON object.)',
    )
    updated_time: Optional[datetime] = Field(
        "",
        description='Timestamp of content update in RFC3339, identical to `created_time` in systems that do not support updates. (This is the update time of the underlying content, not of the JSON object.)',
    )
    version: Optional[str] = Field(
        "",
        description='A string representing a version.\n(Some systems may use checksum, a RFC3339 timestamp, or an incrementing version number.)',
    )
    size: int = Field(
        ...,
        description='For blobs, the blob size in bytes.\nFor bundles, the cumulative size, in bytes, of items in the\n`contents` field.',
    )
    mime_type: Optional[str] = Field(
        "", description='A string providing the mime-type of the `DrsObject`.'
    )
    checksums: List[Checksum] = Field(
        ...,
        description='The checksum of the `DrsObject`. At least one checksum must be provided.\nFor blobs, the checksum is computed over the bytes in the blob.\n\nFor bundles, the checksum is computed over a sorted concatenation of the checksums of its top-level contained objects (not recursive, names not included). The list of checksums is sorted alphabetically (hex-code) before concatenation and a further checksum is performed on the concatenated checksum value.\n\nFor example, if a bundle contains blobs with the following checksums:\nmd5(blob1) = 72794b6d\nmd5(blob2) = 5e089d29\n\nThen the checksum of the bundle is:\nmd5( concat( sort( md5(blob1), md5(blob2) ) ) )\n= md5( concat( sort( 72794b6d, 5e089d29 ) ) )\n= md5( concat( 5e089d29, 72794b6d ) )\n= md5( 5e089d2972794b6d )\n= f7a29a04',
    )
    access_methods: Optional[List[AccessPostMethod]] = Field(
        [],
        description='The list of access methods that can be used to fetch the `DrsObject`.\nRequired for single blobs; optional for bundles.',
    )
    aliases: Optional[List[str]] = Field(
        [],
        description='A list of strings that can be used to find other metadata about this `DrsObject` from external metadata sources. These aliases can be used to represent secondary accession numbers or external GUIDs.',
    )
    contents: Optional[List[ContentsObject]] = Field(
        [],
        description='If not set, this `DrsObject` is a single blob.\nIf set, this `DrsObject` is a bundle containing the listed `ContentsObject` s (some of which may be further nested).',
    )
     


ContentsObject.update_forward_refs()
