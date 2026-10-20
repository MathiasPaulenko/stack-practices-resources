# OPA policy: validate role bindings against forbidden roles
package k8srequiredrolebindings

violation[{"msg": msg}] {
  input.review.object.roleRef.name == "cluster-admin"
  not input.review.object.subjects[_].name in input.parameters.allowedGroups
  msg := sprintf("cluster-admin role cannot be bound to %v", [input.review.object.subjects[_].name])
}
