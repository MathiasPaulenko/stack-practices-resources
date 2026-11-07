# Módulos de Terraform — Módulo de VPC, pruebas y composición

Código complementario de la [Guía Completa de Módulos de Terraform](https://stackpractices.com/es/guides/complete-guide-terraform-modules/) en StackPractices.

## Estructura

```text
modules/vpc/                  # El módulo canónico de la guía
├── main.tf                   # VPC, subnets (for_each), IGW, NAT, route tables
├── variables.tf              # Inputs con bloques de validación
├── outputs.tf                # IDs que referencian los consumidores
├── versions.tf               # required_version + fijación de provider
├── examples/basic/main.tf    # Uso ejecutable (terraform init && plan)
└── tests/vpc.tftest.hcl      # Suite nativa de terraform test
test/vpc_test.go              # Terratest e2e (apply real, tiene coste)
```

## Pruébalo

```bash
cd modules/vpc/examples/basic
terraform init
terraform plan          # renderiza el grafo completo, sin apply
```

Ejecuta las pruebas de contrato desde la raíz del módulo:

```bash
cd modules/vpc
terraform init
terraform test          # corre tests/vpc.tftest.hcl
```

La suite de Terratest despliega recursos reales en AWS (la EIP + NAT gateway tienen coste):

```bash
cd test
go test -v -timeout 30m
```

## Notas

- `for_each = toset(var.public_subnets)` direcciona las subnets por CIDR, así que quitar una entrada a mitad de lista no recrea el resto.
- La route table privada envía `0.0.0.0/0` por el NAT gateway — sin ella, las subnets privadas se crean pero quedan aisladas.
- `azs` puede quedar vacío para usar los defaults de la región en una versión más completa; aquí el ejemplo los pasa explícitamente.
