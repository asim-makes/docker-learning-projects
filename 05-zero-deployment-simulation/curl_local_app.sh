for i in {1..50};
    do curl -s http://localhost:8000/ | grep version;
done
