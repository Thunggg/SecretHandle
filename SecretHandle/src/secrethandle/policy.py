"""Destination matching, intersection, and attenuation for Equation (7)."""

from __future__ import annotations

from typing import FrozenSet, Optional

from .schemas import ConfirmationMode, DestinationPolicy, HandleMetadata, TargetContext


def _matches(values: Optional[FrozenSet[str]], observed: Optional[str], required: bool) -> bool:
    if observed is None and required:
        return False
    if values is None:
        return not required or observed is not None
    if not values:
        return False
    return observed is not None and observed in values


def matches(policy: DestinationPolicy, target: TargetContext) -> bool:
    """Implement Definition 1 and Equation (7), failing closed on required identity."""

    return (
        _matches(policy.packages, target.package, True)
        and _matches(policy.origins, target.origin, policy.require_origin)
        and _matches(policy.fields, target.field_class, policy.require_field)
        and _matches(policy.nodes, target.node_id, policy.require_node)
    )


def _intersect(
    left: Optional[FrozenSet[str]], right: Optional[FrozenSet[str]]
) -> Optional[FrozenSet[str]]:
    if left is None:
        return right
    if right is None:
        return left
    return frozenset(left.intersection(right))


def intersect(left: DestinationPolicy, right: DestinationPolicy) -> DestinationPolicy:
    """Monotonic policy intersection used by Algorithm 1 line 4."""

    return DestinationPolicy(
        packages=_intersect(left.packages, right.packages),
        origins=_intersect(left.origins, right.origins),
        fields=_intersect(left.fields, right.fields),
        nodes=_intersect(left.nodes, right.nodes),
        require_origin=left.require_origin or right.require_origin,
        require_field=left.require_field or right.require_field,
        require_node=left.require_node or right.require_node,
    )


def is_empty(policy: DestinationPolicy) -> bool:
    return any(values is not None and len(values) == 0 for values in (
        policy.packages, policy.origins, policy.fields, policy.nodes
    ))


_CONFIRMATION_STRENGTH = {
    ConfirmationMode.NONE: 0,
    ConfirmationMode.USER: 1,
    ConfirmationMode.PROTECTED: 2,
}


def _subset(child: Optional[FrozenSet[str]], parent: Optional[FrozenSet[str]]) -> bool:
    if parent is None:
        return True
    if child is None:
        return False
    return child.issubset(parent)


def is_safe_attenuation(original: HandleMetadata, candidate: HandleMetadata) -> bool:
    """Implement Proposition 3 for the finite policy language."""

    return (
        original.task_id == candidate.task_id
        and _subset(candidate.destination.packages, original.destination.packages)
        and _subset(candidate.destination.origins, original.destination.origins)
        and _subset(candidate.destination.fields, original.destination.fields)
        and _subset(candidate.destination.nodes, original.destination.nodes)
        and candidate.expires_at <= original.expires_at
        and candidate.use_budget <= original.use_budget
        and _CONFIRMATION_STRENGTH[candidate.confirmation]
        >= _CONFIRMATION_STRENGTH[original.confirmation]
    )
