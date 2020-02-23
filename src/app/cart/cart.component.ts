import { Component, OnInit } from '@angular/core';
import { MainControllerService } from '../services/main-controller.service';
import { ModalController } from '@ionic/angular';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss'],
})
export class CartComponent implements OnInit {

  cart: Array<any>;
  total: number;

  constructor(
    private mainController: MainControllerService,
    private modalController: ModalController,
    ) { 
    this.total = 0;
  }

  ngOnInit() {
    this.getTotal();
  }

  getTotal() {
    this.cart.map(v => {
      this.total += parseInt(v.ProductPrice, 0);
    });
  }

  clearCart() {
    this.mainController.clearCartList();
    this.modalController.dismiss();
  }
}
