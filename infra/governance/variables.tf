variable "subscription_id" {
  description = "Existing full subscription resource ID; supplied by the owning root."
  type        = string
}

variable "allowed_locations_assignment_name" {
  description = "Existing assignment name, preserved verbatim during extraction."
  type        = string
}

variable "allowed_locations_display_name" {
  description = "Existing assignment display name."
  type        = string
}

variable "allowed_locations" {
  description = "Existing allowed-region list, preserving order and values."
  type        = list(string)
}

variable "required_tag_names" {
  description = "Existing tag names; each value remains its for_each key."
  type        = list(string)
}
