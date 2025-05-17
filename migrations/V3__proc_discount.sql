CREATE FUNCTION calculate_discount(amount DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
    RETURN amount * 0.1;
END;
$$ LANGUAGE plpgsql;
