-- Bridgaton AI: multi-tenant PostgreSQL schema baseline

CREATE TABLE organizations (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(120),
    country_code VARCHAR(8) DEFAULT 'NG',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(32) NOT NULL CHECK (role IN ('admin', 'analyst', 'viewer')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE skus (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    sku_code VARCHAR(120) NOT NULL,
    sku_name VARCHAR(255),
    unit_cost NUMERIC(14, 2),
    unit_price NUMERIC(14, 2),
    UNIQUE (organization_id, sku_code)
);

CREATE TABLE locations (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    location_code VARCHAR(120) NOT NULL,
    name VARCHAR(255),
    UNIQUE (organization_id, location_code)
);

CREATE TABLE demand_history (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    sku_id BIGINT NOT NULL REFERENCES skus(id),
    location_id BIGINT REFERENCES locations(id),
    demand_date DATE NOT NULL,
    quantity NUMERIC(14, 4) NOT NULL CHECK (quantity >= 0),
    promo_flag BOOLEAN NOT NULL DEFAULT FALSE,
    unit_price NUMERIC(14, 2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (organization_id, sku_id, location_id, demand_date)
);

CREATE TABLE inventory_snapshots (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    sku_id BIGINT NOT NULL REFERENCES skus(id),
    location_id BIGINT REFERENCES locations(id),
    snapshot_date DATE NOT NULL,
    on_hand NUMERIC(14, 4) NOT NULL CHECK (on_hand >= 0),
    in_transit NUMERIC(14, 4) NOT NULL DEFAULT 0 CHECK (in_transit >= 0)
);

CREATE TABLE supplier_profiles (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    supplier_name VARCHAR(255) NOT NULL,
    lead_time_mean_days NUMERIC(10, 2) NOT NULL,
    lead_time_std_days NUMERIC(10, 2) NOT NULL DEFAULT 0,
    reliability_score NUMERIC(5, 4) NOT NULL DEFAULT 0.95
);

CREATE TABLE forecasts (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    sku_id BIGINT NOT NULL REFERENCES skus(id),
    location_id BIGINT REFERENCES locations(id),
    model_name VARCHAR(64) NOT NULL,
    horizon_date DATE NOT NULL,
    p10 NUMERIC(14, 4) NOT NULL,
    p50 NUMERIC(14, 4) NOT NULL,
    p90 NUMERIC(14, 4) NOT NULL,
    rmse NUMERIC(12, 4),
    mape NUMERIC(8, 6),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE decisions (
    id BIGSERIAL PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    sku_id BIGINT NOT NULL REFERENCES skus(id),
    location_id BIGINT REFERENCES locations(id),
    reorder_quantity NUMERIC(14, 4) NOT NULL,
    reorder_day_offset INTEGER NOT NULL,
    stockout_probability NUMERIC(8, 6) NOT NULL,
    expected_profit_delta_pct NUMERIC(8, 4) NOT NULL,
    cash_tied_inventory NUMERIC(14, 2) NOT NULL,
    confidence_score NUMERIC(8, 6) NOT NULL,
    provenance JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_demand_org_sku_date ON demand_history(organization_id, sku_id, demand_date);
CREATE INDEX idx_forecasts_org_sku_date ON forecasts(organization_id, sku_id, horizon_date);
CREATE INDEX idx_decisions_org_sku_created ON decisions(organization_id, sku_id, created_at);
