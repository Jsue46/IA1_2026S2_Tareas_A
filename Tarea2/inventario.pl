% Hecho: ítems principales del aventurero (al menos 4 ítems, al menos 1 duplicado)
items_principales([espada, pocion, escudo, pocion]).

% Hecho: ítems secundarios del aventurero (al menos 3 ítems distintos)
items_secundarios([mapa, brujula, antorcha]).

% Predicado recursivo para mostrar el inventario
% Aridad: imprimir_inventario/1
% Caso Base: Si la lista está vacía, no hace nada y termina exitosamente.
imprimir_inventario([]).

% Caso Recursivo: desestructurando la lista en Cabeza (H) y Cola (T)
% Imprime la cabeza (ítem actual) y se llama recursivamente con el resto de la lista (T).
imprimir_inventario([H|T]) :-
    writeln(H),
    imprimir_inventario(T).

% Regla Principal de Procesamiento
% Aridad: procesar_inventario/5
% Lógica: Unifica varias variables tras procesar las listas mediante funciones nativas de prolog.
procesar_inventario(ItemBuscado, TotalItems, InventarioInvertido, InventarioUnico, InventarioOrdenado) :-
    % Obtener los ítems principales y secundarios
    items_principales(Principales),
    items_secundarios(Secundarios),
    
    % 1. append/3: concatena las dos listas para formar el Inventario General
    append(Principales, Secundarios, InventarioGeneral),
    
    % 2. length/2: obtiene el total de ítems en el Inventario General
    length(InventarioGeneral, TotalItems),
    
    % 3. member/2: verifica si el ItemBuscado pertenece al Inventario General
    member(ItemBuscado, InventarioGeneral),
    
    % 4. reverse/2: invierte el orden del Inventario General
    reverse(InventarioGeneral, InventarioInvertido),
    
    % 5. sort/2: ordena el inventario y elimina los ítems duplicados (Inventario Único)
    sort(InventarioGeneral, InventarioUnico),
    
    % 6. msort/2: ordena el inventario pero mantiene los duplicados
    msort(InventarioGeneral, InventarioOrdenado),
    
    % Última instrucción: llama a la regla recursiva para imprimir todos los ítems en consola
    imprimir_inventario(InventarioGeneral).
