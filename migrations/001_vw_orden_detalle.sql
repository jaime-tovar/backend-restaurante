-- Vista para ver el detalle completo de las órdenes

CREATE OR REPLACE VIEW vw_orden_detalle AS
SELECT 
    o.id_orden,
    o.estado AS estado_orden,
    o.fecha_creacion,
    m.numero_mesa,
    p.nombre AS nombre_plato,
    d.cantidad,
    d.precio_unitario,
    (d.cantidad * d.precio_unitario) AS total_linea
FROM ordenes o
JOIN mesas m ON o.id_mesa = m.id_mesa
JOIN detalle_orden d ON o.id_orden = d.id_orden
JOIN platos p ON d.id_plato = p.id_plato;