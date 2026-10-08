/**
 * Role Pattern — runnable example.
 *
 * Attach/detach roles on a Person entity at runtime and check
 * capabilities through role objects.
 *
 * Run: node role_pattern.js
 */

class CustomerRole {
  constructor(loyaltyPoints = 0) {
    this.roleName = 'customer';
    this.loyaltyPoints = loyaltyPoints;
  }

  canPerform(action) {
    return ['browse', 'purchase', 'review'].includes(action);
  }

  earnPoints(amount) {
    this.loyaltyPoints += amount;
  }
}

class EmployeeRole {
  constructor(department, salary) {
    this.roleName = 'employee';
    this.department = department;
    this.salary = salary;
  }

  canPerform(action) {
    return ['browse', 'inventory', 'support', 'refund'].includes(action);
  }

  processRefund(orderId) {
    return `Refund processed for ${orderId}`;
  }
}

class VendorRole {
  constructor(companyName, commissionRate = 0.05) {
    this.roleName = 'vendor';
    this.companyName = companyName;
    this.commissionRate = commissionRate;
  }

  canPerform(action) {
    return ['list_products', 'manage_inventory', 'view_sales'].includes(action);
  }
}

class Person {
  constructor(personId, name) {
    this.personId = personId;
    this.name = name;
    this.roles = new Map();
    this.history = [];
  }

  assignRole(role) {
    this.roles.set(role.roleName, role);
    this.history.push({ action: 'assigned', role: role.roleName, timestamp: new Date().toISOString() });
  }

  revokeRole(roleName) {
    if (this.roles.has(roleName)) {
      this.roles.delete(roleName);
      this.history.push({ action: 'revoked', role: roleName, timestamp: new Date().toISOString() });
    }
  }

  hasRole(roleName) {
    return this.roles.has(roleName);
  }

  getRole(roleName) {
    return this.roles.get(roleName);
  }

  canPerform(action) {
    for (const role of this.roles.values()) {
      if (role.canPerform(action)) return true;
    }
    return false;
  }

  getRoleNames() {
    return Array.from(this.roles.keys());
  }
}

// Usage
const person = new Person('P-001', 'Alice');
person.assignRole(new CustomerRole(100));
person.assignRole(new EmployeeRole('Sales', 75000));

console.log('Roles:', person.getRoleNames());
console.log('Can browse:', person.canPerform('browse'));
console.log('Can refund:', person.canPerform('refund'));

const empRole = person.getRole('employee');
if (empRole) console.log(empRole.processRefund('ORD-123'));

person.revokeRole('customer');
console.log('Roles after revoke:', person.getRoleNames());
