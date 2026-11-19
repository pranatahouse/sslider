<?php
/**
 * Mengembalikan URL gambar acak berdasarkan keyword.
 *
 * HTTP:  /random_image.php?q=bali
 * CLI:   php random_image.php bali
 */

$isCli = PHP_SAPI === 'cli';

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST");
header("Access-Control-Allow-Headers: X-Requested-With");

$configPath = __DIR__ . '/../config.base.php';
if (is_file($configPath)) {
    require_once $configPath;
}

function failRequest($message, $httpStatus = 400)
{
    global $isCli;

    if ($isCli) {
        fwrite(STDERR, $message . PHP_EOL);
        exit(1);
    }

    http_response_code($httpStatus);
    header('Content-Type: text/plain; charset=utf-8');
    echo $message . PHP_EOL;
    exit;
}

function normalizeKeyword($value)
{
    $value = str_replace('-', ' ', trim($value));
    if (function_exists('mb_strtolower')) {
        $value = mb_strtolower($value, 'UTF-8');
    } else {
        $value = strtolower($value);
    }

    $normalized = preg_replace('/\s+/u', ' ', $value);
    return trim($normalized === null ? $value : $normalized);
}

$rawKeyword = $isCli
    ? ($argv[1] ?? '')
    : ($_GET['keyword'] ?? $_GET['q'] ?? '');
if (!is_string($rawKeyword)) {
    failRequest('Keyword harus berupa teks.');
}
if (trim($rawKeyword) === 'mantra') {
    $rawKeyword = 'mantra, bali';
}
if (trim($rawKeyword) === '') {
    $rawKeyword = 'bali';
}

$keywords = array();
foreach (explode(',', $rawKeyword) as $providedKeyword) {
    $providedKeyword = normalizeKeyword($providedKeyword);
    if ($providedKeyword !== '' && !in_array($providedKeyword, $keywords, true)) {
        $keywords[] = $providedKeyword;
    }
}
if (count($keywords) === 0) {
    $keywords = array('bali');
}
$keywordLookup = array_fill_keys($keywords, true);
$databasePath = null;
if (defined('SQLITE_BALICANDRA_DB')) {
    $databasePath = constant('SQLITE_BALICANDRA_DB');
} elseif (isset($SQLITE_BALICANDRA_DB)) {
    $databasePath = $SQLITE_BALICANDRA_DB;
}
if (!is_string($databasePath) || trim($databasePath) === '') {
    $databasePath = __DIR__ . '/balicandra.db';
}
if (!is_file($databasePath) || !is_readable($databasePath)) {
    failRequest('Database balicandra.db tidak ditemukan atau tidak bisa dibaca.', 500);
}

try {
    $database = new PDO('sqlite:' . $databasePath, null, null, array(
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ));

    $query = $database->query(
        "SELECT image_url, keywords
         FROM random_images
         WHERE status = 'active' AND image_url IS NOT NULL AND image_url <> ''"
    );

    $matches = array();
    foreach ($query as $row) {
        $terms = explode(',', $row['keywords'] ?? '');
        foreach ($terms as $term) {
            if (isset($keywordLookup[normalizeKeyword($term)])) {
                $matches[] = $row['image_url'];
                break;
            }
        }
    }
} catch (Throwable $error) {
    error_log('random_image.php: ' . $error->getMessage());
    failRequest('Gagal membaca database gambar.', 500);
}

if (count($matches) === 0) {
    failRequest('Tidak ada gambar untuk keyword tersebut.', 404);
}

if (!$isCli) {
    header('Content-Type: text/plain; charset=utf-8');
}
echo $matches[random_int(0, count($matches) - 1)] . PHP_EOL;
