import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


# ============================================================================
# Tests for overage_charge
# ============================================================================

def test_overage_unknown_plan_raises_value_error():
    """Test that an unsupported plan name raises ValueError."""
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("unlimited", 5, False, False)


def test_overage_negative_data_raises_value_error():
    """Test that negative data usage raises ValueError."""
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_overage_within_included_data_no_charge():
    """Test data usage strictly within or equal to included limit yields 0 charge."""
    # Under limit
    assert overage_charge("standard", 3, False, False) == 0
    # Exactly at limit
    assert overage_charge("basic", 2, False, False) == 0
    assert overage_charge("premium", 10, False, False) == 0


def test_overage_loyalty_bonus_non_premium():
    """Loyal customer on basic/standard plan gets +1 GB included data."""
    # Basic has 2 GB; loyal user gets 2 + 1 = 3 GB included
    assert overage_charge("basic", 3, False, True) == 0
    # 4 GB usage: extra is 4 - 3 = 1 GB at 15 rate
    assert overage_charge("basic", 4, False, True) == 15

    # Standard has 5 GB; loyal user gets 5 + 1 = 6 GB included
    assert overage_charge("standard", 6, False, True) == 0
    assert overage_charge("standard", 7, False, True) == 15


def test_overage_loyalty_bonus_premium_plan_excluded():
    """Loyal customer on premium plan does NOT get extra GB included (included remains 10)."""
    # 10 GB is included, extra = 0
    assert overage_charge("premium", 10, False, True) == 0
    # 11 GB usage: extra is 11 - 10 = 1 GB at 15 rate (not 0)
    assert overage_charge("premium", 11, False, True) == 15


def test_overage_extra_within_ten_gb_local():
    """Extra data <= 10 GB under local network (rate = 15)."""
    # basic included = 2; usage = 7; extra = 5; 5 * 15 = 75
    assert overage_charge("basic", 7, False, False) == 75
    # usage = 12; extra = 10 (boundary <= 10); 10 * 15 = 150
    assert overage_charge("basic", 12, False, False) == 150


def test_overage_extra_within_ten_gb_roaming():
    """Extra data <= 10 GB while roaming (rate = 40)."""
    # basic included = 2; usage = 7; extra = 5; 5 * 40 = 200
    assert overage_charge("basic", 7, True, False) == 200
    # usage = 12; extra = 10 (boundary <= 10); 10 * 40 = 400
    assert overage_charge("basic", 12, True, False) == 400


def test_overage_extra_exceeding_ten_gb_local():
    """Extra data > 10 GB under local network (rate = 15 + 10 = 25)."""
    # basic included = 2; usage = 13; extra = 11; 11 * 25 = 275
    assert overage_charge("basic", 13, False, False) == 275


def test_overage_extra_exceeding_ten_gb_roaming():
    """Extra data > 10 GB while roaming (rate = 40 + 10 + 5 = 55)."""
    # basic included = 2; usage = 13; extra = 11; 11 * 55 = 605
    assert overage_charge("basic", 13, True, False) == 605


# ============================================================================
# Tests for recharge_allowed
# ============================================================================

def test_recharge_kyc_pending():
    """When KYC is pending, only amount <= 200 is allowed regardless of pending count."""
    assert recharge_allowed(200, 0, True) is True
    assert recharge_allowed(150, 5, True) is True
    assert recharge_allowed(201, 0, True) is False
    assert recharge_allowed(500, 1, True) is False


def test_recharge_no_kyc_amount_exceeds_max_limit():
    """When KYC is verified, recharge amount > 2000 is rejected."""
    assert recharge_allowed(2001, 0, False) is False
    assert recharge_allowed(5000, 0, False) is False


def test_recharge_no_kyc_pending_recharges_limit():
    """When KYC is verified and amount <= 2000, up to 2 pending recharges are allowed."""
    # pending_recharges <= 2 allowed
    assert recharge_allowed(500, 1, False) is True
    assert recharge_allowed(2000, 2, False) is True
    assert recharge_allowed(100, 0, False) is True

    # pending_recharges > 2 rejected
    assert recharge_allowed(500, 3, False) is False
    assert recharge_allowed(2000, 4, False) is False


# ============================================================================
# Tests for validity_status
# ============================================================================

def test_validity_prepaid_without_addon():
    """Prepaid without addon has cutoff = 0:
    active: days_left >= 0
    grace:  -15 <= days_left < 0
    expired: days_left < -15
    """
    assert validity_status(5, True, False) == "active"
    assert validity_status(0, True, False) == "active"
    assert validity_status(-1, True, False) == "grace"
    assert validity_status(-15, True, False) == "grace"
    assert validity_status(-16, True, False) == "expired"


def test_validity_prepaid_with_addon():
    """Prepaid with addon has cutoff = 2 (0 + 2):
    active: days_left >= 2
    grace:  -13 <= days_left < 2
    expired: days_left < -13
    """
    assert validity_status(2, True, True) == "active"
    assert validity_status(3, True, True) == "active"
    assert validity_status(1, True, True) == "grace"
    assert validity_status(-13, True, True) == "grace"
    assert validity_status(-14, True, True) == "expired"


def test_validity_postpaid_without_addon():
    """Postpaid without addon has cutoff = 3:
    active: days_left >= 3
    grace:  -12 <= days_left < 3
    expired: days_left < -12
    """
    assert validity_status(4, False, False) == "active"
    assert validity_status(3, False, False) == "active"
    assert validity_status(2, False, False) == "grace"
    assert validity_status(-12, False, False) == "grace"
    assert validity_status(-13, False, False) == "expired"


def test_validity_postpaid_with_addon():
    """Postpaid with addon has cutoff = 5 (3 + 2):
    active: days_left >= 5
    grace:  -10 <= days_left < 5
    expired: days_left < -10
    """
    assert validity_status(6, False, True) == "active"
    assert validity_status(5, False, True) == "active"
    assert validity_status(4, False, True) == "grace"
    assert validity_status(-10, False, True) == "grace"
    assert validity_status(-11, False, True) == "expired"
