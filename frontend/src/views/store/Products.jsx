import React, { useState, useEffect } from 'react'
import apiInstance from '../../utils/axios'
import { Link } from 'react-router-dom'
import GetCurrentAddress from '../plugin/UserCountry';
import UserData from '../plugin/UserData';
import CartID from '../plugin/CartID'
import Swal from 'sweetalert2'

const Toast = Swal.mixin({
    toast: true,
    position: "top",
    showConfirmButton: false,
    timer: 1500,
    timeProgressBar: true,
})




function Products() {
    const [products, setProducts] = useState([])
    const [category, setCategory] = useState([])

    const [colorValue, setColorValue] = useState("No Color")
    const [sizeValue, setSizeValue] = useState("No Size")
    const [qtyValue, setQtyValue] = useState(1)


    const [selectedProduct, setSelectedProduct] = useState(null)
    const [selectedColors, setSelectedColors] = useState({})
    const [selectedSize, setSelectedSize] = useState({})

    const currentAddress = GetCurrentAddress()
    const userData = UserData()
    const cart_id = CartID()


    const handleColorButtonClick = (event, product_id, colorName) => {
        setColorValue(colorName);
        setSelectedProduct(product_id)

        setSelectedColors((prevSelectedColors) => ({
            ...prevSelectedColors,
            [product_id]: colorName
        }))
    }

    const handleSizeButtonClick = (event, product_id, sizeName) => {
        setSizeValue(sizeName);
        setSelectedProduct(product_id)

        setSelectedSize((prevSelectedSize) => ({
            ...prevSelectedSize,
            [product_id]: sizeName
        }))
    }
    const handleQtyChange = (event, product_id) => {
        setQtyValue(event.target.value)
        setSelectedProduct(product_id)

    }



    useEffect(() => {
        apiInstance.get(`products/`).then((response) => {

            setProducts(response.data);
        })

    }, [])

    useEffect(() => {
        apiInstance.get("category/")
            .then((response) => setCategory(response.data))
            .catch((error) => console.error("Erro ao buscar categorias:", error));
    }, []);

    const handleAddToCart = async (product_id, price, shipping_amount) => {
        try {
            const formData = new FormData()

            formData.append("product_id", product_id)
            formData.append("user_id", userData?.user_id)
            formData.append("qty", qtyValue)
            formData.append("shipping_amount", shipping_amount)
            formData.append("country", currentAddress.country)
            formData.append("price", price)
            formData.append("size", sizeValue)
            formData.append("color", colorValue)
            formData.append("cart_id", cart_id)

            const response = await apiInstance.post(`cart-view/`, formData)
            console.log(response.data);
            Toast.fire({
                icon: "success",
                title: response.data.message
            })


        } catch (error) {
            console.log(error);

        }

    }


    return (
        <>
            <main className="mt-5">
                <div className="container">
                    <section className="text-center">
                        <div className="row">
                            {products?.map((p, index) => (

                                <div className="col-lg-4 col-md-12 mb-4" key={index}>
                                    <div className="card">
                                        <div
                                            className="bg-image hover-zoom ripple"
                                            data-mdb-ripple-color="light"
                                        >
                                            <Link to={`detail/${p.slug}/`}>
                                                <img
                                                    src={p.image}
                                                    className="w-100 img-fluid"
                                                    style={{ height: "300px", objectFit: "cover" }}
                                                />
                                            </Link>
                                            {/* <a href="#!">
                                                <div className="mask">
                                                    <div className="d-flex justify-content-start align-items-end h-100">
                                                        <h5>
                                                            <span className="badge badge-primary ms-2">New</span>
                                                        </h5>
                                                    </div>
                                                </div>
                                                <div className="hover-overlay">
                                                    <div
                                                        className="mask"
                                                        style={{ backgroundColor: "rgba(251, 251, 251, 0.15)" }}
                                                    />
                                                </div>
                                            </a> */}
                                        </div>
                                        <div className="card-body">
                                            <Link to={`detail/${p.slug}/`} className="text-reset">
                                                <h5 className="card-title mb-3">{p.title}</h5>
                                            </Link>
                                            <a href="" className="text-reset">
                                                <p>{p.category?.title}</p>
                                            </a>
                                            <div className="d-flex justify-content-center">
                                                <h6 className="mb-3">${p.price}</h6>
                                                <h6 className="mb-3 text-muted ms-2"><strike>${p.old_price}</strike></h6>
                                            </div>
                                            <div className="btn-group">
                                                <button
                                                    className="btn btn-primary dropdown-toggle"
                                                    type="button"
                                                    id="dropdownMenuClickable"
                                                    data-bs-toggle="dropdown"
                                                    data-bs-auto-close="false"
                                                    aria-expanded="false"
                                                >
                                                    Variation
                                                </button>
                                                <ul
                                                    className="dropdown-menu"
                                                    aria-labelledby="dropdownMenuClickable"
                                                >

                                                    <div className="d-flex flex-column">
                                                        <li className="p-1">
                                                            <b>Quantity</b>:
                                                        </li>
                                                        <div className="p-1 mt-0 pt-0 d-flex flex-wrap">

                                                            <li>
                                                                <input
                                                                    className='form-control'
                                                                    type="number"
                                                                    onChange={(e) => handleQtyChange(e, p.id)}
                                                                />
                                                            </li>
                                                        </div>
                                                    </div>

                                                    {p.size?.length > 0 &&
                                                        <div className="d-flex flex-column">
                                                            <li className="p-1">
                                                                <b>Size</b>: {selectedSize[p.id] || "NoSize"}
                                                            </li>
                                                            <div className="p-1 mt-0 pt-0 d-flex flex-wrap">
                                                                {p.size?.map((s, index) => (

                                                                    <li key={index}>
                                                                        <button
                                                                            className="btn btn-secondary btn-sm me-2 mb-1"
                                                                            onClick={(e) => handleSizeButtonClick(e, p.id, s.name)}

                                                                        >
                                                                            {s.name}
                                                                        </button>
                                                                    </li>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    }

                                                    {p.size?.length > 0 &&
                                                        <div className="d-flex flex-column mt-3">
                                                            <li className="p-1">
                                                                <b>Color</b>:{selectedColors[p.id] || "No Color"}
                                                            </li>
                                                            <div className="p-1 mt-0 pt-0 d-flex flex-wrap">
                                                                {p.color?.map((c, index) => (

                                                                    <li key={index}>
                                                                        <button
                                                                            className="btn btn-sm me-2 mb-1 p-3"
                                                                            style={{ backgroundColor: c.color_code }}
                                                                            onClick={(e) => handleColorButtonClick(e, p.id, c.name)}
                                                                        />
                                                                    </li>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    }
                                                    <div className="d-flex mt-3 p-1">
                                                        <button
                                                            type="button"
                                                            className="btn btn-primary me-1 mb-1"
                                                            onClick={() => handleAddToCart(p.id, p.price, p.shipping_amount)}
                                                        >
                                                            <i className="fas fa-shopping-cart" />
                                                        </button>
                                                        <button
                                                            type="button"
                                                            className="btn btn-danger px-3 me-1 mb-1 ms-2"
                                                        >
                                                            <i className="fas fa-heart" />
                                                        </button>
                                                    </div>
                                                </ul>
                                                <button
                                                    type="button"
                                                    className="btn btn-danger px-3 me-1 ms-2"
                                                >
                                                    <i className="fas fa-heart" />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            ))}

                            <div className='row'>
                                {category?.map((c, index) => (

                                    <div className="col-lg-2" key={index}>
                                        <img src={c.image} style={{ width: "100px", height: "100px", borderRadius: "50%", objectFit: "cover" }} alt="" />
                                        <h6>{c.title}</h6>
                                    </div>
                                ))}
                            </div>

                        </div>
                    </section>
                    {/*Section: Wishlist*/}
                </div>
            </main>
        </>
    )
}

export default Products
