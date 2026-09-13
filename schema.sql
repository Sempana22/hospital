-- ═══════════════════════════════════════════════════════════════════════
-- Schema: Kuesioner Kepuasan Pasien — RSUD SLG Kediri
-- Database: Supabase PostgreSQL
-- ═══════════════════════════════════════════════════════════════════════

-- 1. Create the responses table
CREATE TABLE IF NOT EXISTS responses (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at      TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    respondent_code TEXT NOT NULL,
    nama_pasien     TEXT,
    umur            NUMERIC(4,1) NOT NULL,
    jenis_kelamin   TEXT NOT NULL,
    lama_dirawat    TEXT NOT NULL,
    q1              INT NOT NULL CHECK (q1 BETWEEN 1 AND 5),
    q2              INT NOT NULL CHECK (q2 BETWEEN 1 AND 5),
    q3              INT NOT NULL CHECK (q3 BETWEEN 1 AND 5),
    q4              INT NOT NULL CHECK (q4 BETWEEN 1 AND 5),
    q5              INT NOT NULL CHECK (q5 BETWEEN 1 AND 5),
    q6              INT NOT NULL CHECK (q6 BETWEEN 1 AND 5),
    q7              INT NOT NULL CHECK (q7 BETWEEN 1 AND 5),
    q8              INT NOT NULL CHECK (q8 BETWEEN 1 AND 5),
    q9              INT NOT NULL CHECK (q9 BETWEEN 1 AND 5),
    q10             INT NOT NULL CHECK (q10 BETWEEN 1 AND 5),
    q11             INT NOT NULL CHECK (q11 BETWEEN 1 AND 5),
    q12             INT NOT NULL CHECK (q12 BETWEEN 1 AND 5),
    saran           TEXT
);

-- Migration for databases created before q12 was added.
ALTER TABLE responses
    ADD COLUMN IF NOT EXISTS q12 INT CHECK (q12 BETWEEN 1 AND 5);

-- 2. Index on created_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_responses_created_at ON responses (created_at DESC);

-- 3. Index on respondent_code for lookups
CREATE INDEX IF NOT EXISTS idx_responses_code ON responses (respondent_code);

-- 4. Enable Row Level Security (RLS)
ALTER TABLE responses ENABLE ROW LEVEL SECURITY;

-- 5. Policy: Public can INSERT (anonymous submission)
CREATE POLICY "Allow anonymous insert"
    ON responses
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- 6. Policy: Anon can SELECT everything.
--    IMPORTANT: this app's "admin login" (see auth.py) is an application-level
--    check (username/password stored in Streamlit secrets), NOT Supabase Auth.
--    The Streamlit app always connects to Supabase with the anon key, so if
--    anon cannot SELECT, every admin page (Dashboard, Data Responden,
--    Statistik, Saran & Kritik, Export Data) will fail with a permissions
--    error even after a successful app login. Admin-page access is already
--    gated in the app itself (auth.require_admin()), so it is safe to allow
--    anon SELECT here.
CREATE POLICY "Allow read for anon (app-level admin gate)"
    ON responses
    FOR SELECT
    TO anon
    USING (true);

-- 7. Policy: Authenticated/service-role can also SELECT everything, in case
--    you later switch to a service_role key or real Supabase Auth.
CREATE POLICY "Allow full read for authenticated"
    ON responses
    FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Allow full read for service_role"
    ON responses
    FOR SELECT
    TO service_role
    USING (true);

-- ═══════════════════════════════════════════════════════════════════════
-- Notes:
--   - The app uses the anon key via st.secrets["SUPABASE_KEY"] for both
--     reading and writing (see database.py).
--   - INSERT is allowed for anon (public submissions).
--   - SELECT is allowed for anon too, because admin access is enforced at
--     the application layer, not via Supabase Auth roles.
--   - For stronger security in production, switch to the service_role key
--     (kept server-side only) and remove the anon SELECT policy above.
-- ═══════════════════════════════════════════════════════════════════════
