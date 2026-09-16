#!/usr/bin/env bash
# Deployment rollback quick-reference for kubectl, Helm, and ArgoCD.
# Usage: source this file or copy the function you need. Set APP and NS first.
#
#   export APP=my-app NS=production
#   rollback_kubectl        # revert Deployment to previous revision
#   rollback_kubectl_to 3   # revert to a specific revision
#   rollback_helm           # revert Helm release to previous revision
#   rollback_helm_to 5      # revert to revision 5
#   verify_rollback         # image, pods, events, health check

APP="${APP:-my-app}"
NS="${NS:-production}"

rollback_kubectl() {
    kubectl rollout history "deployment/$APP" -n "$NS"
    kubectl rollout undo "deployment/$APP" -n "$NS"
    kubectl rollout status "deployment/$APP" -n "$NS"
}

rollback_kubectl_to() {
    local rev="${1:?revision number required}"
    kubectl rollout undo "deployment/$APP" -n "$NS" --to-revision="$rev"
    kubectl rollout status "deployment/$APP" -n "$NS"
}

rollback_helm() {
    helm history "$APP" -n "$NS"
    helm rollback "$APP" -n "$NS" --timeout 5m
}

rollback_helm_to() {
    local rev="${1:?revision number required}"
    helm rollback "$APP" "$rev" -n "$NS" --timeout 5m
}

verify_rollback() {
    kubectl get deployment "$APP" -n "$NS" \
        -o jsonpath='{.spec.template.spec.containers[*].image}'
    echo
    kubectl get pods -n "$NS" -l "app=$APP" -o wide
    kubectl logs "deployment/$APP" -n "$NS" --tail=50
    kubectl get events -n "$NS" \
        --field-selector "involvedObject.name=$APP" --sort-by='.lastTimestamp'
}

argocd_git_revert() {
    # GitOps rollback: revert the commit, push, let ArgoCD sync.
    # Preferred over `argocd app rollback`, which is imperative and
    # fights auto-sync (the change is not persisted in Git).
    local sha="${1:?bad commit sha required}"
    git revert "$sha" && git push origin main
    argocd app sync "$APP"   # only needed if auto-sync is disabled
}
