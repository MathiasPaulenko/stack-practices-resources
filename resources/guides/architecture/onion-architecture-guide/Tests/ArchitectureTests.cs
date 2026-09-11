using System.Reflection;
using Xunit;

namespace OnionArchitecture.Tests;

/// <summary>
/// Architecture tests that enforce the dependency rule:
/// dependencies must point inward, never outward.
/// Domain must not reference Infrastructure, Application, or Presentation.
/// </summary>
public class ArchitectureTests
{
    private static readonly Assembly DomainAssembly = typeof(Domain.Entities.Order).Assembly;
    private static readonly Assembly ApplicationAssembly = typeof(Application.Orders.PlaceOrder.PlaceOrderHandler).Assembly;
    private static readonly Assembly InfrastructureAssembly = typeof(Infrastructure.Messaging.InMemoryEventBus).Assembly;

    [Fact]
    public void Domain_ShouldNot_ReferenceInfrastructure()
    {
        var domainRefs = DomainAssembly.GetReferencedAssemblies().Select(a => a.Name);
        Assert.DoesNotContain("Microsoft.EntityFrameworkCore", domainRefs);
        Assert.DoesNotContain("Infrastructure", domainRefs);
    }

    [Fact]
    public void Domain_ShouldNot_ReferencePresentation()
    {
        var domainRefs = DomainAssembly.GetReferencedAssemblies().Select(a => a.Name);
        Assert.DoesNotContain("Microsoft.AspNetCore", domainRefs);
        Assert.DoesNotContain("Presentation", domainRefs);
    }

    [Fact]
    public void Application_ShouldNot_ReferenceInfrastructure()
    {
        var appRefs = ApplicationAssembly.GetReferencedAssemblies().Select(a => a.Name);
        Assert.DoesNotContain("Microsoft.EntityFrameworkCore", appRefs);
        Assert.DoesNotContain("Infrastructure", appRefs);
    }

    [Fact]
    public void Application_ShouldNot_ReferencePresentation()
    {
        var appRefs = ApplicationAssembly.GetReferencedAssemblies().Select(a => a.Name);
        Assert.DoesNotContain("Microsoft.AspNetCore", appRefs);
        Assert.DoesNotContain("Presentation", appRefs);
    }

    [Fact]
    public void Domain_ShouldNot_ReferenceApplication()
    {
        var domainRefs = DomainAssembly.GetReferencedAssemblies().Select(a => a.Name);
        Assert.DoesNotContain("Application", domainRefs);
    }

    [Fact]
    public void Infrastructure_Should_ReferenceDomain()
    {
        var infraRefs = InfrastructureAssembly.GetReferencedAssemblies().Select(a => a.Name);
        Assert.Contains("Domain", infraRefs);
    }
}
