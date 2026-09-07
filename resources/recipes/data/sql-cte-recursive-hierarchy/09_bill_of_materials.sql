-- Bill of materials explosion.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 09_bill_of_materials.sql

WITH RECURSIVE bom AS (
    -- Anchor: top-level assembly
    SELECT
        component_id,
        assembly_id,
        quantity,
        1 AS level,
        CAST(component_id AS VARCHAR(1000)) AS component_path
    FROM bill_of_materials
    WHERE assembly_id = 'PRODUCT-001'

    UNION ALL

    -- Recursive: components of components
    SELECT
        b.component_id,
        b.assembly_id,
        b.quantity * bom.quantity AS total_quantity,
        bom.level + 1,
        bom.component_path || ' -> ' || CAST(b.component_id AS VARCHAR)
    FROM bill_of_materials b
    INNER JOIN bom ON b.assembly_id = bom.component_id
)
SELECT
    component_id,
    level,
    total_quantity,
    component_path
FROM bom
ORDER BY level, component_id;
