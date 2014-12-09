$name = $args[0]
if($null -eq $name){
    $collections = Get-RDSessionCollection
    if($collections.count -eq 0){
        echo 'Error. No session collections available!'
        exit 1
    }
    # Just use the first avail. collection
    $name = $collections[0].CollectionName
    echo $name
}
echo 'before'
Get-RDAvailableApp -CollectionName $name
echo 'after'