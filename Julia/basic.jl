using Printf
using Statistics


function bubble_sort!(a)
    n=length(a)
    for i in 1:n-1
        for j in 1:n-i
            if a[j]>a[j+1]
                a[j], a[j+1] = a[j+1], a[j]
            end
        end
    end
    return a
end

data = [65,51,2,1,23,84,68,3]
bubble_sort!(data)
